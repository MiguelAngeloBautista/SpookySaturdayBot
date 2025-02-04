"""
Spooky Saturday Bot
"""

import os

from dotenv import load_dotenv
from discord import Intents
from discord.ext import commands
from discord.ext.commands import Context

from poll import Poll
from logger import log

TESTING: bool = True # Set to False when deploying to production. Changes guild to 0, bypasses date time check pylint: disable=C0301

intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name="hi")
async def send_hello(ctx: Context):
    """
    Sends a "Hello World!" message to the Discord channel.
    """
    await ctx.send("Hello World!")

@bot.command(name="commands")
async def send_help(ctx: Context):
    """
    Sends a help message with the available commands to the Discord channel.
    """
    await ctx.send("Hello! I'm the Spooky Saturday bot. "
                   "I can help you with the Spooky Saturday poll. "
                   "Polls are held every Monday and the results are announced on Saturday at 8pm. "
                   "You may reannounce the results by using the !pollresult command. ")

@bot.event
async def on_ready():
    """
    Event handler for the bot's on_ready event.
    """
    log("APP", f"Logged in as {bot.user.name} at {[guild.name for guild in bot.guilds]}")
    await bot.add_cog(Poll(bot, TESTING))
    poll = bot.get_cog('Poll')
    bot.loop.create_task(poll.send_spooky_saturday(TESTING))


if __name__ == "__main__":
    load_dotenv()

    log("APP", "Starting Spooky Saturday Bot")
    
    if TESTING:
        log("APP", "Running in testing mode. GUILD_INDEX set to 0. Bypassing date-time check.")

    if "BOT_TOKEN" in os.environ:
        bot.run(os.getenv("BOT_TOKEN"))

    else:
        log("APP", "BOT_TOKEN not found in environment variables. Exiting.")
        exit()
