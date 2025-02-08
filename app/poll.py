"""
A module to manage and handle the Spooky Saturday poll within a Discord bot.
"""

import datetime
import asyncio
import json
from typing import Literal, Optional

from discord.ext.commands import Cog, command, Context, Bot
from discord import Embed, NotFound, Message, TextChannel

from app.logger import INFO_LOG, ERROR_LOG

#Type Aliases
ChannelID = int
PollID = int

class Poll(Cog):
    """
    A class to manage and handle the Spooky Saturday poll within a Discord bot.
    
    ### Attributes:
        `bot (commands.Bot)`: The Discord bot instance.
        `options (dict)`: A dictionary mapping game names to their corresponding emoji.
        `poll (dict)`: A dictionary mapping channel IDs to message IDs for active polls.
    ### Methods:
        `__init__(self, bot)`:
            Initializes the Poll class with the bot instance and sets up options and poll attributes.
        `check_poll_results(self, ctx)`:
            Manually checks the results of the Spooky Saturday poll and sends a message with the results.
        `automatic_check_poll_results(self)`:
            Automatically checks the results of the Spooky Saturday poll every Saturday at 8 PM and sends a message with the results.
        `send_spooky_saturday(self)`:
            Sends a "Happy Spooky Saturday!" message to a specific Discord channel if today is Saturday.
    
    """
    GUILD_INDEX = 1 # Guild Index for the bot to send messages to 0 = Testing, 1 = Main

    def __init__(self, bot: Bot, testing: bool = False):
        self.bot: Bot = bot
        self.options = {
            "Phasmophobia 👻": "👻",
            "Lethal Company 🚀": "🚀",
            "Oh deer 🦌": "🦌",
            "Content Warning ⚠️": "⚠️",
            "Panicore 🧱": "🧱",
            "Nuclear Nightmare 🌨️": "🌨️",
            "Backrooms ☣️": "☣️",
            "Murky Divers 🤿": "🤿",
            "Devour ✝️": "✝️",
            "Subterranauts 🌕": "🌕",
            "Dark Hours 💎": "💎",
            "Kletka 🛗": "🛗",
            "GTFO 😶": "😶",
            "Factorio ⚙️": "⚙️",
            "JackBox 📦": "📦"
        }
        self.poll: dict[ChannelID, PollID] = {}

        if testing is True:
            self.GUILD_INDEX = 0 # pylint: disable=C0103
        
    async def get_wait_time(self, day_name: str, time: int = 0, log_message: str = None) -> tuple[int, float]:

    async def get_wait_time(self, day_name: Literal["monday", "tuesday", "wednesday","thursday", "friday", "saturday", "sunday"], time: int = 0, log_message: str = None) -> tuple[int, float]:
        """
        Waits until the next specified day of the week at the given time.
        
        ### Example:
            `await get_wait_time("Monday", 20)`:  Waits until the next Monday at 8:00 PM (24-hour format)
        ### Args:
            `day_name (str)`: The name of the day to wait for (e.g., "Monday").
            `time (int)`: The time to wait for in 24-hour format (e.g., 20 for 8 PM).
            `log_message (Optional[str])`: A message to log when waiting. Defaults to None.

        ### Returns:
            `timestamp (int)`: The timestamp of the next target day in seconds.
            `wait_time (float)`: The time to wait in seconds.
        """
        days_of_week = ["monday", "tuesday", "wednesday",
                        "thursday", "friday", "saturday", "sunday"]
        now = datetime.datetime.now()

        try:
            target_daytime = days_of_week.index(day_name.lower())
        except ValueError as exc:
            raise ValueError("Invalid day name. Please use a valid day name "
                             "(e.g., 'Monday')") from exc

        days_until_target = (target_daytime - now.weekday() + 7) % 7
        next_target_day = now + datetime.timedelta(days=days_until_target)

        next_target_day = next_target_day.replace(
                hour=time, minute=0, second=0, microsecond=0)

        wait_time = (next_target_day - now).total_seconds()

        INFO_LOG(f"Waiting until {next_target_day} "
            f"{'for ' + log_message if log_message is not None else ''}")

        timestamp = int(next_target_day.timestamp())
        return timestamp, wait_time

    async def wait_until(self, wait_time: float) -> None:
        """
        Waits for a specified amount of time in seconds.

        ### Args:
            `wait_time (float)`: The time to wait in seconds.

        ### Returns:
            None
        """
        INFO_LOG(f"Waiting for {wait_time} seconds...")
        await asyncio.sleep(wait_time)
        INFO_LOG("Wait done... Continuing")

    async def get_poll_message(self, ctx: Context = None) -> Message:
        """
        This function retrieves the poll message from the specified Discord channel
        and stores the message ID in the poll attribute.
        
        ### Args:
            `ctx (Optional[Context])`: The context of the command. Defaults to None.
            
        ### Note:
            This function assumes that the bot instance and the channel ID are correctly set up.
        
        ### Returns:
            `poll_message (discord.Message)`: The poll message from the specified Discord channel.
        """
        poll_message = None
        for channel_id, message_id in self.poll.items():
            channel = self.bot.get_channel(channel_id)
            if not channel:
                continue  # Skip if channel is unavailable
            if ctx is not None and channel.guild != ctx.guild:
                continue  # Skip if channel is in a different guild only if ctx is provided

            try:
                poll_message = await channel.fetch_message(message_id)
            except NotFound:
                continue  # Skip if poll message was deleted
        return poll_message

    async def calculate_results(self, poll_message: Message) -> str:
        """
        This function calculates the results of the Spooky Saturday poll
        and returns the winner(s) and the result text.

        ### Args:
            `poll_message (discord.Message)`: The poll message from the specified Discord channel.

        ### Returns:
            `result_text (str)`: The result text of the poll.
        """
        # Count reactions (subtract 1 to ignore bot's reaction)
        reactions = {reaction.emoji: reaction.count - 1 for reaction in poll_message.reactions}

        result_text = ""
        for option, emoji in self.options.items():
            votes = reactions.get(emoji, 0)
            result_text += f"{option}: {votes} votes\n"

        max_votes = max(reactions.values())

        if reactions:
            winners = [option for option, emoji in self.options.items() if reactions.get(emoji, 0) == max_votes]
            # winners = [option for option, votes in reactions.items() if votes == max_votes]

            if len(winners) == 1:
                result_text += f"\nWinner: {winners[0]}"
            elif max_votes == 0:
                result_text += "\nNo Votes"
            else:
                result_text += f"\nTie: {', '.join(winners)}"
        else:
            result_text += "\nNo Votes"

        return result_text

    @command(name="pollresult")
    async def check_poll_results(self, ctx: Context):
        """
        Manually check the results of the Spooky Saturday poll 
        and sends a message with the results.

        This function retrieves the poll results and 
        sends a message with the results to the specified Discord channel.

        ### Note:
            This function assumes that the bot instance and the channel ID are correctly set up.

        ### Returns:
            None
        """
        poll_message: Message = await self.get_poll_message(ctx)
        if poll_message is None:
            await ctx.send("No active poll found.")
            return
        result_text = await self.calculate_results(poll_message)

        results_embed = Embed(title="Spooky Saturday Poll Results",
                            description=result_text,
                            color=0x00FF00,
                            timestamp=datetime.datetime.now())

        await ctx.send(embed=results_embed)

    async def automatic_check_poll_results(self, bypass: bool = False, wait_time: int = 0) -> None:
        """
        Checks the results of the Spooky Saturday poll every Saturday at 8pm~ 
        and sends a message with the results.

        This function retrieves the poll results and 
        sends a message with the results to the specified Discord channel.

        ### Args:
            `bypass (Optional[bool])`: Whether to bypass the wait time. Defaults to False.
            `timestamp (Optional[int])`: The timestamp for the next target day in seconds since the epoch. Defaults to 0.
            `wait_time (Optional[int])`: The time to wait in seconds. Defaults to 0.

        ### Note:
            This function assumes that the bot instance and the channel ID are correctly set up.

        ### Returns:
            None
        """
        poll_message: Message = await self.get_poll_message()
        if poll_message is None:
            ERROR_LOG("No active poll found.")
            return
        channel: TextChannel = poll_message.channel
        
        if bypass:
            wait_time = 0
            INFO_LOG("Bypassing wait time for poll results check")

        await self.wait_until(wait_time)

        result_text = await self.calculate_results(poll_message)

        results_embed = Embed(title="Spooky Saturday Poll Results",
                              description=result_text,
                              color=0x00FF00,
                              timestamp=datetime.datetime.now())

        await channel.send(embed=results_embed)
        
        if bypass:
            await self.wait_until(86400)  # Wait for one day before checking again
        
    async def send_spooky_saturday(self, bypass: bool = False) -> None:
        """
        Sends a "Happy Spooky Saturday!" message to a specific Discord channel if today is Monday.
        This function checks the current day of the week, and if it is Monday (weekday() == 0),
        it retrieves the specified Discord channel and sends the Spooky Saturday Poll message.
        
        ### Args:
            `bypass (Optional[bool])`: Whether to bypass the wait time. Defaults to False.

        ### Note:
            This function assumes that the bot instance and the channel ID are correctly set up.

        ### Returns:
            None
        """
        while not self.bot.is_closed():
            next_saturday = None

            if not bypass:
                INFO_LOG("Checking for Spooky Saturday... " +
                    str(datetime.date.today().weekday()))

                wait_time = await self.get_wait_time("Monday", log_message="next poll")
                await self.wait_until(wait_time[1])

                today = datetime.date.today()
                next_saturday = today + datetime.timedelta((5 - today.weekday() + 7) % 7)
            else:
                INFO_LOG("Bypassing date-time Check...")

            message = None
            poll_channel = None

            poll_channel, message = await self.check_existing_poll_message()
            if message is None:
                poll_channel, message = await self.send_new_poll_message(next_saturday)

                    message = await channel.send(

            _, result_wait_time = await self.get_wait_time("Saturday", 20, log_message="next poll results")
            await self.automatic_check_poll_results(wait_time=result_wait_time)

            if not bypass:
                await self.wait_until(86400) # Sleep for a day

            if poll_channel is not None:
                self.poll.pop(poll_channel.id)
                await self.save_poll()

            ### Use For When Discord decides to allow more than 10 options in a poll ###
            # question = f"Spooky Saturday ({next_saturday.strftime('%d/%m')}): " + \
            #     "Please check the pinned messages for game info, prices and sales. " + \
            #     "Please feel free to recommend games 😊"

            # poll = Poll(question=question, duration=datetime.timedelta(hours=168), multiple=True)
            # print(len(options))
            # for option in options:
            #     print(option)
            #     poll.add_answer(text=option, emoji=option[-1])

            # await channel.send(poll=poll)
    
    async def check_existing_poll_message(self) -> tuple[Optional[TextChannel], Optional[Message]]:
        """
        Checks for existing poll messages in the specified Discord channel.

        ### Returns:
            `poll_channel (Optional[TextChannel])`: The channel where the poll message was found.
            `message (Optional[Message])`: The existing poll message.
        """
        for channel in self.bot.guilds[self.GUILD_INDEX].text_channels:
            if channel.id in self.poll.keys():
                message_id = self.poll.get(channel.id)
                message: Message = await channel.fetch_message(message_id)
                adelaide_time = message.created_at + datetime.timedelta(hours=10.5)  # Convert UTC to Adelaide time (UTC+10:30)
                INFO_LOG(f"Existing Poll Message: {message_id} made: {adelaide_time.strftime('%d %B %Y %H:%M:%S')} in {channel.name} at {channel.guild.name}")
                return channel, message_id
        return None, None
    
    async def send_new_poll_message(self, next_saturday: datetime.date) -> tuple[Optional[TextChannel], Optional[Message]]:
        """
        Sends a new poll message to the specified Discord channel.

        ### Args:
            `next_saturday (datetime.date)`: The date of the next Saturday.

        ### Returns:
            `poll_channel (Optional[TextChannel])`: The channel where the poll message was sent.
            `message (Optional[Message])`: The new poll message.
        """
        for channel in self.bot.guilds[self.GUILD_INDEX].text_channels:
            if channel.name == "spooky-saturday":
                INFO_LOG(f"Found spooky-saturday channel in {self.bot.guilds[self.GUILD_INDEX].name}. Sending Message...")

                message = await channel.send(
                    f"Spooky Saturday ({next_saturday.strftime('%d/%m') if next_saturday is not None else ''}): "
                    "Please check the pinned messages for game info, prices and sales. "
                    "Please feel free to recommend games 😊 "
                    "\n\n(Chosen game will be decided by 8pm)\n\n"
                    f"{'\n'.join(self.options.keys())}") # noqa: E999
                self.poll[channel.id] = message.id

                # Optimize adding reactions using asyncio.create_task
                tasks = [asyncio.create_task(message.add_reaction(option)) for option in self.options.values()]
                await asyncio.gather(*tasks)
                INFO_LOG(f"Added reactions to message {message.id} in channel {channel.name}")

                timestamp, result_wait_time = await self.get_wait_time("Saturday", 20, log_message="next poll results")
                await channel.send(f"Poll results will be announced <t:{timestamp}:R>")

                return channel, message
        return None, None
