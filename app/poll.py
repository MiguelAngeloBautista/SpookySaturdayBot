"""
A module to manage and handle the Spooky Saturday poll within a Discord bot.
"""
# pylint: disable=E0401,E0611
import datetime
import asyncio

from discord.ext.commands import Cog, command
from discord import Embed, NotFound

from logger.logger import log

class Poll(Cog):
    """
    A class to manage and handle the Spooky Saturday poll within a Discord bot.
    Attributes:
        bot (commands.Bot): The Discord bot instance.
        options (dict): A dictionary mapping game names to their corresponding emoji.
        poll (dict): A dictionary mapping channel IDs to message IDs for active polls.
    Methods:
        __init__(self, bot):
            Initializes the Poll class with the bot instance and sets up options and poll attributes.
        check_poll_results(self, ctx):
            Manually checks the results of the Spooky Saturday poll and sends a message with the results.
        automatic_check_poll_results(self):
            Automatically checks the results of the Spooky Saturday poll every Saturday at 8 PM and sends a message with the results.
        send_spooky_saturday(self):
            Sends a "Happy Spooky Saturday!" message to a specific Discord channel if today is Saturday.
    
    """

    def __init__(self, bot):
        self.bot = bot
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
        self.poll = {}

    @command(name="pollresult")
    async def check_poll_results(self, ctx):
        """
        Manually check the results of the Spooky Saturday poll 
        and sends a message with the results.

        This function retrieves the poll results and 
        sends a message with the results to the specified Discord channel.

        Note:
            This function assumes that the bot instance and the channel ID are correctly set up.

        Returns:
            None
        """
        # Check results for current poll (Potential for multiple polls)
        for channel_id, message_id in self.poll.items():
            channel = self.bot.get_channel(channel_id)
            if not channel:
                continue  # Skip if channel is unavailable

            try:
                poll_message = await channel.fetch_message(message_id)
            except NotFound:
                continue  # Skip if poll message was deleted

        # Count reactions (subtract 1 to ignore bot's reaction)
        reactions = {reaction.emoji: reaction.count - 1 for reaction in poll_message.reactions}


        result_text = ""
        for option, emoji in self.options.items():
            votes = reactions.get(emoji, 0)
            result_text += f"{option}: {votes} votes\n"

        max_votes = max(reactions.values())
        winners = [option for option, votes in reactions.items() if votes == max_votes]

        if len(winners) == 1:
            result_text += f"\nWinner: {winners[0]}"
        else:
            result_text += f"\nTie: {', '.join(winners)}"

        results_embed = Embed(title="Spooky Saturday Poll Results",
                            description=result_text,
                            color=0x00FF00,
                            timestamp=datetime.datetime.now())

        # await channel.send(embed=results_embed)
        await ctx.send(embed=results_embed)

    async def automatic_check_poll_results(self):
        """
        Checks the results of the Spooky Saturday poll every Saturday at 8pm~ 
        and sends a message with the results.

        This function retrieves the poll results and 
        sends a message with the results to the specified Discord channel.

        Note:
            This function assumes that the bot instance and the channel ID are correctly set up.

        Returns:
            None
        """
        # while True:
        now = datetime.datetime.now()
        target_time = now.replace(hour=20, minute=0, second=0, microsecond=0)  # 8:00 PM

        # If today is not Saturday, find the next one
        days_until_saturday = (5 - now.weekday()) % 7  # 5 = Saturday (Monday is 0)
        target_time += datetime.timedelta(days=days_until_saturday)

        # Time to wait until next Saturday 8 PM
        wait_time = (target_time - now).total_seconds()
        log(f"Waiting until {target_time} for next poll result...")

        # Check results for all channels with active polls
        for channel_id, message_id in self.poll.items():
            channel = self.bot.get_channel(channel_id)
            if not channel:
                continue  # Skip if channel is unavailable

            try:
                poll_message = await channel.fetch_message(message_id)
            except NotFound:
                continue  # Skip if poll message was deleted

        timestamp = int(target_time.timestamp())
        await channel.send(f"Poll results will be announced <t:{timestamp}:R>")

        await asyncio.sleep(wait_time)  # Wait until Saturday 8 PM


        # Count reactions (subtract 1 to ignore bot's reaction)
        reactions = {reaction.emoji: reaction.count - 1 for reaction in poll_message.reactions}

        result_text = ""
        for option, emoji in self.options.items():
            votes = reactions.get(emoji, 0)
            result_text += f"{option}: {votes} votes\n"

        max_votes = max(reactions.values())
        winners = [option for option, votes in reactions.items() if votes == max_votes]

        if len(winners) == 1:
            result_text += f"\nWinner: {winners[0]}"
        else:
            result_text += f"\nTie: {', '.join(winners)}"

        results_embed = Embed(title="Spooky Saturday Poll Results",
                            description=result_text,
                            color=0x00FF00,
                            timestamp=datetime.datetime.now())

        await channel.send(embed=results_embed)

        # await asyncio.sleep(86400)  # Wait 24 hours before checking again to avoid double results

    async def send_spooky_saturday(self):
        """
        Sends a "Happy Spooky Saturday!" message to a specific Discord channel if today is Saturday.

        This function checks the current day of the week, and if it is Monday (weekday() == 0),
        it retrieves the specified Discord channel and sends the Spooky Saturday Poll message.

        Note:
            This function assumes that the bot instance and the channel ID are correctly set up.

        Returns:
            None
        """
        while True:
            log("Checking for Spooky Saturday... " + str(datetime.date.today().weekday()))
            # print(f"{BColour.BLACK}{datetime.datetime.now()}{BColour.OFF} "
            #     f"{BColour.CYAN}APP{BColour.OFF} Checking for Spooky Saturday... " +
            #     str(datetime.date.today().weekday()))

            now = datetime.datetime.now()
            next_monday = now + datetime.timedelta(days=(7 - now.weekday()) % 7)  # Find next Monday
            next_monday = next_monday.replace(hour=0,
                minute=0, second=0, microsecond=0)  # Set to midnight
            wait_time = (next_monday - now).total_seconds()

            await asyncio.sleep(wait_time)  # Wait until Monday

            # channel = self.bot.get_channel(1114128548895129631)
            today = datetime.date.today()
            next_saturday = today + datetime.timedelta((5 - today.weekday() + 7) % 7)

            message = None
            poll_channel = None

            for channel in self.bot.guilds[0].text_channels:
                if channel.name == "spooky-saturday":
                    log(f"Found spooky-saturday channel in {self.bot.guilds[0].name}. "
                        "Sending Message...")

                    message = await channel.send("Spooky Saturday "
                        f"({next_saturday.strftime('%d/%m')}): "
                        "Please check the pinned messages for game info, prices and sales. "
                        "Please feel free to recommend games 😊 "
                        "\n\n(Chosen game will be decided by 8pm)\n\n"
                        f"{'\n'.join(self.options.keys())}")
                    self.poll[channel.id] = message.id
                    poll_channel = channel


            for option in self.options.values():
                await message.add_reaction(option)

            await self.automatic_check_poll_results()

            await asyncio.sleep(86400) # Sleep for a day

            self.poll.pop(poll_channel.id)


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
