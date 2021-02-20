import discord
import os
from discord.ext import commands
import config
import tool

if __name__ == "__main__":
    intents = discord.Intents.all()
    app = commands.AutoShardedBot(command_prefix=config.BotSettings.prefix, intents=intents)

    app.remove_command("help")
    for filename in os.listdir("Cogs"):
        if filename.endswith(".py"):
            app.load_extension(f"Cogs.{filename[:-3]}")

    if config.BotSettings.TEST_mode == True:
        print("TEST mode On")
        TOKENs = config.BotSettings.TESTBOT_TOKEN
    else: TOKENs = config.BotSettings.TOKEN

    app.run(TOKENs, bot=True, reconnect=True)