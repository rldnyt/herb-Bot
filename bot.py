import discord
import os
from discord.ext import commands
import config
import tool
import asyncio
import discord
import json
import os
import logging
import websockets
import time
import koreanbots
import tool
from discord import Webhook, RequestsWebhookAdapter


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
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


    async def change_presence():
        sleep_time = config.BotSettings.statetime
        await app.wait_for("ready")
        while True:
            if len(config.BotSettings.state) == 1:
                await app.change_presence(activity=discord.Game(config.BotSettings.state[0]))
                await asyncio.sleep(sleep_time)
                continue
            for x in config.BotSettings.state:
                try:
                    await app.change_presence(activity=discord.Game(x))
                    await asyncio.sleep(sleep_time)
                except (asyncio.streams.IncompleteReadError, discord.ConnectionClosed,
                        websockets.exceptions.ConnectionClosedError):
                    await asyncio.sleep(sleep_time)
                except Exception: await asyncio.sleep(sleep_time)


    loop.create_task(change_presence())

    app.run(TOKENs, bot=True, reconnect=True)