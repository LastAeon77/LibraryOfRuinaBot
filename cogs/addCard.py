# import aiohttp
# from discord.ext import commands
# from utils.checks import owner_check
# from utils.csvEdits import append_list_as_row
# import os
# import aiofiles


# class AddCard(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot

#     @commands.command()
#     async def exist(self, ctx):
#         """Test is AddCard Exists"""
#         await ctx.send("I exist lol")

#     @commands.command()
#     @commands.check(owner_check)
#     async def addCombatPage(self, ctx, *, arx: str):
#         """Enter things in this order: Class(Urban nightmare etc),
#         Office(wedge etc),Id,Chapter,Obtainable,Cost,Name,CardImgLink(url),
#         Score(Not Important),Rarity,On Play Effects,DiceNumber,D1 Type,D1 Roll,
#         D1 Effect,
#         D2 Type,D2 Roll,D2 Effect,D3 Type,D3 Roll,D3 Effect,D4 Type,D4 Roll,
#         Effect"""
#         dataRow = arx.split(",")
#         _class = dataRow[0]
#         _office = dataRow[1]
#         dataRow = dataRow[2:]
#         if len(dataRow) < 12:
#             await ctx.send("Not enough information")
#         else:
#             # "Card\Urban Myth\Pierre\Basic_StongStrike.png"
#             dir = os.path.join("Card", _class)
#             if not os.path.exists(dir):
#                 os.mkdir(dir)
#             dir = os.path.join("Card", _class, _office)
#             if not os.path.exists(dir):
#                 os.mkdir(dir)
#             link = dataRow[5]
#             dataRow[5] = f"Card/{_class}/{_office}/{dataRow[4]}.png"
#             append_list_as_row("./data/CardData.csv", dataRow)
#             await self.fetchImage(link, dataRow[5])
#             await ctx.send("Process is done")

#     # Source: https://stackoverflow.com/
#     # questions/35388332/how-to-download-images-with-aiohttp
#     async def fetchImage(self, url, path):
#         async with aiohttp.ClientSession() as session:
#             async with session.get(str(url)) as resp:
#                 if resp.status == 200:
#                     f = await aiofiles.open(path, mode="wb")
#                     await f.write(await resp.read())
#                     await f.close()


# def setup(bot):
#     bot.add_cog(AddCard(bot))


# # "Urban Temp, tempOff,23232,5,TRUE,2,EdgeFucks,
# # https://i.ytimg.com/vi/1TagqS3IGIM/maxresdefault.jpg,,PaperBack,,1,Slash,1-1,"
