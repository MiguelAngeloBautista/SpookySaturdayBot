"""
Spooky Saturday Bot
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from discord import Intents
from discord.ext import commands
from discord.ext.commands import Context, DefaultHelpCommand
from colorist import BrightColor as BColour

from app.poll import Poll
from app.logger import INFO_LOG, WARN_LOG

TESTING: bool = True # Set to False when deploying to production. Changes guild to 0, bypasses date time check pylint: disable=C0301

intents = Intents.default()
intents.message_content = True

class CustomHelpCommand(DefaultHelpCommand):
    """
    A Class to overwrite the DefaultHelpCommand class. Sends a custom help_text and all the commands available
    """
    def __init__(self):
        super().__init__()
    
    async def send_bot_help(self, mapping):
        command_list = ""
        
        for cog in mapping:
            commands = [command for command in mapping[cog]]
            command_list += "\n"
            if commands:
                command_list += "\n".join([f"`!{command.name}` - {command.short_doc}" for command in commands])
        
        help_text = (
            "# Hello! I'm the Spooky Saturday bot.\n\n"
            "I can help you with the Spooky Saturday poll. "
            "Polls are held every Monday and the results are announced on Saturday at 8pm. "
            "You may reannounce the results by using the !pollresult command.\n"
            "## Available Commands:\n"
            f"{command_list}\n"
            "\nType !help command for more info on a command."
        )
        await self.get_destination().send(f"{help_text}")
        # return await super().send_bot_help(mapping)
    
    async def send_cog_help(self, cog):
        return await super().send_cog_help(cog)
    
    async def send_group_help(self, group):
        return await super().send_group_help(group)
    
    async def send_command_help(self, command):
        help_text = (
            f"## Command: !{command.name}\n\n"
            f"{command.help}\n"
            "### Usage:\n"
            f"`!{command.qualified_name} {command.signature}`\n"
            f"{'### Description:\n' if command.description != "" else ""}"
            f"{command.description if command.description != "" else ""}\n"
        )
        await self.get_destination().send(f"{help_text}")

bot = commands.Bot(command_prefix='!', intents=intents, help_command=CustomHelpCommand())

@bot.command(name="hi")
async def send_hello(ctx: Context) -> None:
    """
    Sends a "Hello World!" message to the Discord channel.
    """
    await ctx.send("Hello World!")

@bot.event
async def on_ready():
    """
    Event handler for the bot's on_ready event.
    """
    INFO_LOG(f"Logged in as {bot.user.name} at {[guild.name for guild in bot.guilds]}")
    await bot.add_cog(Poll(bot, TESTING))
    poll = bot.get_cog('Poll')
    bot.loop.create_task(poll.send_spooky_saturday(TESTING))

if __name__ == "__main__":
    load_dotenv()

    INFO_LOG("Starting Spooky Saturday Bot")

    if TESTING:
        WARN_LOG(f"Running in {BColour.RED}TESTING MODE{BColour.OFF}. "
                 "GUILD_INDEX set to 0. Bypassing date-time check.", context="SERVER")

    if "BOT_TOKEN" in os.environ:
        bot.run(os.getenv("BOT_TOKEN"))

    else:
        INFO_LOG("BOT_TOKEN not found in environment variables. Exiting.")
        exit()
