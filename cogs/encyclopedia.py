from discord.ext import commands
import discord
import sqlite3


class Encyclopedia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def pedia(self, ctx):
        pass

    @pedia.command()
    async def topic(self, ctx, *, arx: str):
        data = []
        with sqlite3.connect("./data/Encyclopedia.db") as f:
            conn = f.cursor()
            SEARCHTERM = f"""
                SELECT * FROM LorEncyclopedia
                WHERE lower(Sub_Topic) LIKE lower("{arx}")
                """
            conn.execute(SEARCHTERM)
            data = conn.fetchone()
        embed = discord.Embed()
        embed.set_author(name=data[2])
        embed.set_footer(
            text=f"Source: https://docs.google.com/document/d/1GgJD0sVchy_OxAoCWPcLIeGDRoRT3WJdvKDYmMdX-kg/edit?usp=sharing. ID: {data[0]}"
        )
        embed.description = data[3]
        embed.color = 16580705
        await ctx.send(embed=embed)

    @pedia.command()
    async def id(self, ctx, *, arx: int):
        data = []
        with sqlite3.connect("./data/Encyclopedia.db") as f:
            conn = f.cursor()
            SEARCHTERM = f"""
                SELECT * FROM LorEncyclopedia
                WHERE InfoID={arx}
                """
            conn.execute(SEARCHTERM)
            data = conn.fetchone()
        embed = discord.Embed()
        embed.set_author(name=data[2])
        embed.set_footer(
            text=f"Source: https://docs.google.com/document/d/1GgJD0sVchy_OxAoCWPcLIeGDRoRT3WJdvKDYmMdX-kg/edit?usp=sharing. ID: {data[0]}"
        )
        embed.description = data[3]
        embed.color = 16580705
        await ctx.send(embed=embed)

    async def cutout(self, seq, idx):
        return seq[:idx] + seq[idx + 1 :]

    @pedia.command()
    async def catalogue(self, ctx, arx: int):
        if arx > 7 or arx < 1:
            await ctx.send("Enter number between 1-7")
            return

        with sqlite3.connect("./data/Encyclopedia.db") as f:
            conn = f.cursor()
            SEARCHTERM = f"""
                SELECT * FROM LorEncyclopedia
                WHERE InfoID BETWEEN {arx*10000} AND {arx*10000+10000-1}
                """
            conn.execute(SEARCHTERM)
            data = conn.fetchall()
        embed = discord.Embed()
        embed.set_author(name=f"{data[0][1]}")
        embed.set_footer(
            text="Source: https://docs.google.com/document/d/1GgJD0sVchy_OxAoCWPcLIeGDRoRT3WJdvKDYmMdX-kg/edit?usp=sharing"
        )
        finalStr = ""
        for stuff in data:
            if not len(finalStr) > 2000:
                finalStr += f"> ID: {stuff[0]}  {stuff[2]}"
                finalStr += "\n"
        # if len(finalStr) >= 2048:
        #     while len(finalStr) >= 2048:
        #         substr = finalStr.split("\n")
        #         await self.cutout(substr, len(substr) // 2)
        #         finalStr = ("\n").join(substr)

        embed.color = 16580705
        embed.description = finalStr
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Encyclopedia(bot))
