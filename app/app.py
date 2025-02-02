"""
Spooky Saturday Bot
"""
# pylint: disable=E0401,E0611
import os

from dotenv import load_dotenv
from discord import Intents
from discord.ext import commands

from poll import Poll
from logger.logger import log

intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name="hi")
async def send_hello(ctx):
    """
    Sends a "Hello World!" message to the Discord channel.
    """
    await ctx.send("Hello World!")

@bot.command(name="commands")
async def send_help(ctx):
    """
    Sends a help message with the available commands to the Discord channel.
    """
    await ctx.send("Hello! I'm the Spooky Saturday bot. "
                "I can help you with the Spooky Saturday poll. "
                "Polls are held every Monday and the results are announced on Saturday at 8pm. "
                "You May reannounce the results by using the !pollresult command. ")

@bot.event
async def on_ready():
    """
    Event handler for the bot's on_ready event.
    """
    log(f"Logged in as {bot.user.name}")
    await bot.add_cog(Poll(bot))
    poll = bot.get_cog('Poll')
    bot.loop.create_task(poll.send_spooky_saturday())


if __name__ == "__main__":
    load_dotenv()

    if "BOT_TOKEN" in os.environ:
        bot.run(os.getenv("BOT_TOKEN"))

    else:
        print("No bot token found in .env file")
        exit()
