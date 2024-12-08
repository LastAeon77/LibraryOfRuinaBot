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

dynamic_commands = {}
dynamic_commands_lock = asyncio.Lock()
# Function to add a new dynamic command
def add_dynamic_command(name, image_url):
    async def dynamic_command(ctx):
        await ctx.send(image_url)

    # Add the command to the bot
    bot.add_command(commands.Command(dynamic_command, name=name))
    dynamic_commands[name] = image_url

# Add a command to create new commands dynamically
@bot.command()
async def addcmd(ctx, command_name: str, image_url: str):
    if ctx.message.author.id == bot.config["discord"]["owner"]:
        if command_name in dynamic_commands:
            bot.remove_command(command_name)
        add_dynamic_command(command_name, image_url)
        await ctx.send(f"Command `{command_name}` has been added!")
        await command_save()
        

async def command_load():
    async with dynamic_commands_lock:
        with open("./data/custom_commands.json",'r') as f:
            try:
                curr_data = json.loads(f.read())
                dynamic_commands = curr_data
                for k,v in dynamic_commands.items():
                    add_dynamic_command(k,v)
            except Exception as e:
                print(f"Error saving commands: {e}")

async def command_save():
    async with dynamic_commands_lock:
        with open("./data/custom_commands.json",'w') as f:
            f.write(json.dumps(dynamic_commands))

@bot.event
async def on_ready():
    """Tells owner that bot is ready"""
    synced = await bot.tree.sync()
    # 718294958573879347
    print("Logged in as")
    print(bot.user.name)
    print("------")
    await command_load()

@bot.command()
async def custom_cmds(ctx):
    await ctx.send("``` \n"+ json.dumps(list(dynamic_commands.keys())) + "```")

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
async def numpeople(ctx):
    total = 0
    for guilds in bot.guilds:
        total += guilds.member_count
    await ctx.send(f"has {total} users")


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
            # file == limbus.py is for testing only
            if file.endswith(".py"):  # and file=="limbus.py":
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
