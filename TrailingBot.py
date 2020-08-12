import discord
from discord.ext import commands
import random

#wikipedia
import wikipedia
import pandas as pd
from CardData import Card
from GuildAndToken import TOKEN
from GuildAndToken import GUILD
from OtherOptions import OtherOptions

bot = commands.Bot(command_prefix=commands.when_mentioned_or("?"))


#bot = commands.Bot(command_prefix='?')
@bot.command()
async def search(ctx, *, arx: str):

    name = arx

    try:
        CardTemp = Card(name)
        embed = discord.Embed()
        embed.color = 3066993
        embed.set_author(name=str(arx))
        embed.description = CardTemp.toString()
        embed.add_field(name="Dice Rolls", value=CardTemp.diceDmgStr, inline=True)
        embed.add_field(name="Dice Effects",
                        value=CardTemp.diceEffStr,
                        inline=True)
        embed.add_field(name="Dice Type", value=CardTemp.diceTypeStr, inline=True)
        file = discord.File(CardTemp.imageLink, filename="image.png")
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
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


@bot.command()
async def wiki(ctx, arx: str):
    cont = wikipedia.page(arx)
    ans = ''
    ans += '**' + cont.title + '**' + '\n'
    ans += cont.content
    await ctx.channel.send(ans[0:200])


@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send('{0.name} joined in {0.joined_at}'.format(member))


bot.run(TOKEN)