import discord
from discord.ext import commands
import json
import random
import os
import logging
from logging.handlers import RotatingFileHandler
import asyncio
from discord import app_commands

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or("?"), intents=intents)
# bot.synced = False

with open("resources/settings.json", "r") as f:
    bot.config = json.load(f)

bot.UPDATE_NOTICE = ""


@bot.event
async def on_ready():
    """Tells owner that bot is ready"""
    await bot.tree.sync()
    # 718294958573879347
    print("Logged in as")
    print(bot.user.name)
    print("------")


@bot.command()
async def bestGirl(ctx, arx: str, arx2: str):
    """Tells who best girl is"""
    random.seed()
    if random.randint(1, 100) < 50:
        await ctx.send(arx)
    else:
        await ctx.send(arx2)


@bot.command()
async def update_update(ctx, *, arx: str):
    if ctx.message.author.id == bot.config["discord"]["owner"]:
        bot.UPDATE_NOTICE = arx
        await ctx.send(f"The message has been updated to {arx}")
    else:
        await ctx.send("You are not allowed to use this command")


@bot.command()
async def update(ctx):

    await ctx.send(bot.UPDATE_NOTICE)


@bot.command()
async def num(ctx):
    await ctx.send(f"in {len(bot.guilds)} servs")


@bot.command()
async def damnyouPM(ctx):
    await ctx.send("https://imgur.com/wAHRx0q")


@bot.command()
async def faith(ctx):
    await ctx.send("Have Faith")
    await ctx.send("https://i.imgur.com/hafVVUO.png")


@bot.command()
async def geb(ctx):
    await ctx.send("https://i.imgur.com/4f6kLyt.png")


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


@bot.command()
async def hhpp(ctx):
    """Gives link to HamhamPangPang Registration"""
    await ctx.send(
        r"https://m.place.naver.com/restaurant/1873966909/booking?query=%ED%96%84%ED%96%84%ED%8C%A1%ED%8C%A1"
    )


async def main():
    async with bot:
        for file in os.listdir("cogs"):
            if file.endswith(".py"):
                try:
                    await bot.load_extension("cogs." + os.path.splitext(file)[0])
                    print(f"Extension {file} loaded.")
                except Exception as e:
                    print(f"Failed to load extension {file}: {e}")
        # eating too much space so I stop using logging.
        # logger = logging.getLogger("discord")
        # logger.setLevel(logging.DEBUG)
        # handler = RotatingFileHandler(
        #     filename="data/discord.log",
        #     encoding="utf-8",
        #     mode="a",
        #     maxBytes=5 * 1024 * 1024,
        #     backupCount=2,
        # )
        # handler.setFormatter(
        #     logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
        # )
        # logger.addHandler(handler)
        # bot.run(bot.config["discord"]["token"])
        await bot.start(bot.config["discord"]["token"])


asyncio.run(main())
