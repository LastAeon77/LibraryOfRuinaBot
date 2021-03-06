import sqlite3
from discord.ext import commands
import discord
import os
from utils.deckMakerUtils import (
    TABLENAME,
    DECK_SCHEMA,
    DECK_INSERT,
    DECKSPATH,
    getPrevID,
    checkExist,
    returnImageLink,
    deckImgMaker,
)


class DeckMake(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with sqlite3.connect(DECKSPATH) as file:
            file.execute(DECK_SCHEMA)

    @commands.group()
    async def deck(self, ctx):
        """This command has been removed. Make deck in website instead!"""
        if ctx.invoked_subcommand is None:
            await ctx.send("Make your deck at: http://aeonmoon.herokuapp.com/lor/deck/add/ ! \n Call deck with ?sdeck <id> ")

    # @deck.command()
    # async def code(self, ctx, arx: int):
    #     """Check List of Deck with deck ID"""
    #     with sqlite3.connect(DECKSPATH) as c:
    #         cur = c.cursor()
    #         cur.execute(
    #             f"""SELECT * FROM {TABLENAME}
    #                         WHERE deck_code={arx}"""
    #         )
    #         data = cur.fetchone()
    #         embed = discord.Embed()
    #         embed.set_author(name=str(data[1]))
    #         embed.set_footer(text=f"Code: {data[0]}, Creator: {data[2]}")
    #         ans = f"""Cards:\n
    #                 > {data[3]}
    #                 > {data[4]}
    #                 > {data[5]}
    #                 > {data[6]}
    #                 > {data[7]}
    #                 > {data[8]}
    #                 > {data[9]}
    #                 > {data[10]}
    #                 > {data[11]}
    #                 """
    #         embed.description = ans
    #         embed.color = 3447003
    #         deckImgLink = returnImageLink(data[3:])
    #         finalImg = deckImgMaker(deckImgLink)
    #         finalImg.save("tmp/tmp.png")
    #         file = discord.File("tmp/tmp.png", filename="image.png")
    #         embed.set_image(url="attachment://image.png")
    #         return await ctx.send(file=file, embed=embed)
    #         os.remove("tmp/tmp.png")

    # @deck.command()
    # async def name(self, ctx, *, arx: str):
    #     """Check List of Deck with name"""
    #     with sqlite3.connect(DECKSPATH) as c:
    #         cur = c.cursor()
    #         cur.execute(
    #             f"""SELECT * FROM {TABLENAME}
    #                         WHERE deck_name LIKE '{arx}'"""
    #         )
    #         data = cur.fetchone()
    #         embed = discord.Embed()
    #         embed.set_author(name=str(data[1]))
    #         embed.set_footer(text=f"Code: {data[0]}, Creator: {data[2]}")
    #         ans = f"""Cards:\n
    #                 > {data[3]}
    #                 > {data[4]}
    #                 > {data[5]}
    #                 > {data[6]}
    #                 > {data[7]}
    #                 > {data[8]}
    #                 > {data[9]}
    #                 > {data[10]}
    #                 > {data[11]}
    #                 """
    #         embed.description = ans
    #         embed.color = 3447003
    #         deckImgLink = returnImageLink(data[3:])
    #         finalImg = deckImgMaker(deckImgLink)
    #         finalImg.save("tmp/tmp.png")
    #         file = discord.File("tmp/tmp.png", filename="image.png")
    #         embed.set_image(url="attachment://image.png")
    #         return await ctx.send(file=file, embed=embed)
    #         os.remove("tmp/tmp.png")

    # @deck.command()
    # async def add(self, ctx, *, arx: str):
    #     """This format: deck_name, card #1,card#2,...card#9 **NO WHITE SPACE
    #      BEFORE OR AFTER COMMA**"""
    #     cardNames = arx.split(",")
    #     username = str(ctx.author)
    #     if len(cardNames) != 10:
    #         await ctx.send("Please type in proper syntax")
    #     # print(type(username))
    #     else:
    #         if checkExist(cardNames):
    #             try:
    #                 # print(f"get username: {username}")
    #                 deck_code = getPrevID() + 1
    #                 # print(f"get deckcode: {deck_code}")
    #                 with sqlite3.connect(DECKSPATH) as c:
    #                     cur = c.cursor()
    #                     cur.execute(
    #                         DECK_INSERT,
    #                         (
    #                             deck_code,
    #                             cardNames[0],
    #                             username,
    #                             cardNames[1],
    #                             cardNames[2],
    #                             cardNames[3],
    #                             cardNames[4],
    #                             cardNames[5],
    #                             cardNames[6],
    #                             cardNames[7],
    #                             cardNames[8],
    #                             cardNames[9],
    #                         ),
    #                     )
    #                 await ctx.send(
    #                     f"""Your deck has been added! Deck code is:{deck_code}
    #                     Deck name is: {cardNames[0]}"""
    #                 )
    #             except sqlite3.IntegrityError:
    #                 await ctx.send(
    #                     f"""Your deckname:{cardNames[0]} is
    #                 already taken! Be more original"""
    #                 )
    #         else:
    #             await ctx.send("Some of your cards might've not existed!")

    # @deck.command()
    # async def mydeck(self, ctx):
    #     """This will output all the deck you've made"""
    #     ans = ""
    #     username = str(ctx.author)
    #     with sqlite3.connect(DECKSPATH) as c:
    #         cur = c.cursor()
    #         cur.execute(
    #             f"""SELECT * FROM {TABLENAME}
    #             WHERE creator_name='{username}'"""
    #         )
    #         data = cur.fetchall()
    #         for stuff in data:
    #             ans += stuff[1]
    #             ans += f"|| Deck Code: {stuff[0]}" + "\n"
    #     embed = discord.Embed()
    #     embed.set_author(name=f"{username}'s decks")
    #     embed.description = ans
    #     embed.color = 3447003
    #     await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(DeckMake(bot))
