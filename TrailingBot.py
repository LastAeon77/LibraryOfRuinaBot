import discord
from discord.ext import commands
import json
import random

# wikipedia
# import pandas as pd

from CustomClasses.CardData import Card

# from CustomClasses.GuildAndToken import TOKEN
# from CustomClasses.GuildAndToken import GUILD
from CustomClasses.OtherOptions import OtherOptions

import os

bot = commands.Bot(command_prefix=commands.when_mentioned_or("?"))
with open("resources/settings.json", "r") as f:
    bot.config = json.load(f)


# bot = commands.Bot(command_prefix='?')
@bot.command()
async def search(ctx, *, arx: str):
    """Searches for card in the library"""
    name = arx

    try:
        CardTemp = Card(name)
        embed = discord.Embed()
        embed.color = 3066993
        embed.set_author(name=str(arx))
        embed.description = CardTemp.toString()
        embed.add_field(name="Dice Rolls", value=CardTemp.diceDmgStr, inline=True)
        embed.add_field(name="Dice Effects", value=CardTemp.diceEffStr, inline=True)
        embed.add_field(name="Dice Type", value=CardTemp.diceTypeStr, inline=True)
        file = discord.File(CardTemp.imageLink, filename="image.png", spoiler=True)
        embed.set_image(url="attachment://image.png")
        await ctx.send(file=file, embed=embed)

    except:
        Others = OtherOptions(name)
        mewembed = discord.Embed()
        mewembed.color = 3066993
        mewembed.set_author(name=f"We couldn't find {str(arx)}, Did you mean: \n")
        mewembed.description = Others.toString()
        await ctx.send(embed=mewembed)


@bot.event
async def on_ready():
    """Tells owner that bot is ready"""
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
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
async def update(ctx):
    """Tells who best girl is"""
    random.seed()
    ans = random.randint(1, 10)
    await ctx.send(f"Project moon will update in {ans} hours")


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


if __name__ == "__main__":  # check if in main
    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            try:
                bot.load_extension("cogs." + os.path.splitext(file)[0])
                print(f"Extension {file} loaded.")
            except Exception as e:
                print(f"Failed to load extension {file}: {e}")

    bot.run(bot.config["discord"]["token"])
