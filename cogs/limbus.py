import discord.context_managers
from discord.ext import commands
from discord import app_commands
import discord
from rapidfuzz import fuzz, process
import json

# import tweepy
from utils.cardScrape import get_site_content_json, get_site_request_logged_in
from CustomClasses.limbusData import identity_data_analysis, ego_data_analysis


LINK_LIMBUS_TWITTER = "https://socialblade.com/twitter/user/liberarelimbus"
LINK = "https://malcute.aeonmoon.page"

YOUTUBE_USERNAME = "ProjectMoonOfficial"

FILE_NAME_TWITTER = "./data/twitter_count.txt"
FILE_NAME_YOUTUBE = "./data/youtube_count.txt"
FILE_NAME_TIME = "./data/time_stamp.txt"
IMAGE_LOCATION = "data/follower_graph.png"


class DeleteEmbedView(discord.ui.View):
    def __init__(self, author, message=None):
        super().__init__()
        self.author = author
        self.message = message

    @discord.ui.button(label="Delete", style=discord.ButtonStyle.red)
    async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.author:
            await interaction.message.delete()


class Limbus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.youtube_sub = None
        self.twitter_follow = None
        self.below_150000 = True
        with open("./data/EN_Personalities.json", encoding="utf-8") as f:
            self.iden_dict = json.load(f)
        self.iden_dict = self.iden_dict["dataList"]
        self.identities_list = [
            (x["title"].replace("\n", " ") + x["name"]) for x in self.iden_dict
        ]
        self.identities_num = [
            (int(x["id"]), (x["title"].replace("\n", " ") + " " + x["name"]))
            for x in self.iden_dict
        ]
        with open("./data/EN_Egos.json", encoding="utf-8") as f:
            ego_dict = json.load(f)
        ego_dict = ego_dict["dataList"]

        def until_comma(string):
            final_str = []
            for i in range(len(string)):
                if string[i] == "’" or string[i] == "'":
                    return "".join(final_str)
                final_str.append(string[i])
            return "".join(final_str)

        self.ego_list = [
            (x["name"].replace("\n", " ") + " " + until_comma(x["desc"]))
            for x in ego_dict
        ]
        self.ego_num = [
            (
                int(x["id"]),
                (x["name"].replace("\n", " ") + " " + until_comma(x["desc"])),
            )
            for x in ego_dict
        ]

        # with open("./data/Limbus_Data/EN_BattleKeywords.json",encoding="utf-8") as f:
        #     keyword_dict = json.load(f)
        # keyword_dict = self.keyword_dict["dataList"]
        # self.BattleKeyword = {}
        # for dicts in keyword_dict:
        #     self.BattleKeyword[dicts.get("id","")] = dicts.get("name","")

    async def fuzzy_search(self, query, choices):
        best_match = process.extractOne(
            query.lower(), choices, processor=None, scorer=fuzz.ratio
        )
        best_match = best_match[0]
        best_match = best_match.split("|")
        return best_match

    async def identity_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ):
        identities = self.identities_num
        return [
            discord.app_commands.Choice(name=iden[1], value=str(iden[0]))
            for iden in identities
            if current.lower() in iden[1].lower()
        ]

    async def ego_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ):
        egos = self.ego_num
        return [
            discord.app_commands.Choice(name=ego[1], value=str(ego[0]))
            for ego in egos
            if current.lower() in ego[1].lower()
        ]

    @app_commands.command()
    @app_commands.autocomplete(identities=identity_autocomplete)
    async def identity(
        self, interaction: discord.Interaction, identities: str, uptie_level: int = 4
    ):
        """Test only"""
        data = await get_site_request_logged_in(
            f"https://malcute.aeonmoon.page/api/limbus2/identity_data/{identities}"
        )
        await identity_data_analysis(interaction, data, uptie_level, 45)

    @app_commands.command()
    @app_commands.autocomplete(ego=ego_autocomplete)
    async def ego_limbus(
        self, interaction: discord.Interaction, ego: str, uptie_level: int = 4
    ):
        """Test only"""
        data = await get_site_request_logged_in(
            f"https://malcute.aeonmoon.page/api/limbus2/ego_data/{ego}"
        )
        await ego_data_analysis(interaction, data, uptie_level)


async def setup(bot):
    await bot.add_cog(Limbus(bot))
