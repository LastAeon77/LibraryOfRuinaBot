# import sqlite3
# from discord.ext import commands
# import discord
# import os
# from utils.deckMakerUtils import (
#     TABLENAME,
#     DECK_SCHEMA,
#     DECK_INSERT,
#     DECKSPATH,
#     getPrevID,
#     checkExist,
#     returnImageLink,
#     deckImgMaker,
# )


# class DeckMake(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
#         with sqlite3.connect(DECKSPATH) as file:
#             file.execute(DECK_SCHEMA)

#     # @commands.group()
#     # async def deck(self, ctx):
#     #     """This command has been removed. Make deck in website instead!"""
#     #     if ctx.invoked_subcommand is None:
#     #         await ctx.send(
#     #             "Make your deck at: http://aeonmoon.herokuapp.com/lor/deck/add/ ! \n Call deck with ?sdeck <id> "
#     #         )


# def setup(bot):
#     bot.add_cog(DeckMake(bot))
