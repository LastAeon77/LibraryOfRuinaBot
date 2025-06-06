import discord.context_managers
from discord.ext import commands
from discord import app_commands
import discord
from rapidfuzz import fuzz, process
import json
import os
import re
from PIL import Image, ImageEnhance
import requests
from io import BytesIO
import aiohttp
import asyncio
import random

# import tweepy
from utils.cardScrape import get_site_content_json, get_site_request_logged_in, get_site_post_logged_in
from CustomClasses.limbusData import (
    identity_data_analysis,
    ego_data_analysis,
    battle_keyword_dict,
    story_data_display
)


LINK_LIMBUS_TWITTER = "https://socialblade.com/twitter/user/liberarelimbus"
LINK = "https://malcute.aeonmoon.page"

YOUTUBE_USERNAME = "ProjectMoonOfficial"

FILE_NAME_TWITTER = "./data/twitter_count.txt"
FILE_NAME_YOUTUBE = "./data/youtube_count.txt"
FILE_NAME_TIME = "./data/time_stamp.txt"
IMAGE_LOCATION = "data/follower_graph.png"
BETS_FILE = "./data/bet.json"

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

        # Gift Section
        self.gift_data = {}
        for file in os.listdir("./data/Limbus_Data"):
            if file.startswith("EN_EGOgift_"):
                with open(f"./data/Limbus_Data/{file}", encoding="utf-8") as f:
                    data = json.load(f)
                    for dicts in data.get("dataList", []):
                        self.gift_data[dicts.get("id", 0)] = dicts
        self.gift_num = []
        for k, v in self.gift_data.items():
            self.gift_num.append((k, v.get("name")))

        # Abnormality Observations
        self.observation_data, self.observation_num = self.observation_dict_generate()

        self.battlekeyword_data, self.battlekeyword_num = self.battlekeyword_dict_generate()

        self.gift_tier_data = self.ego_gift_tier_generate()
        
        self.en_chapter_node_list = self.EnChapterNodeList_dict_generate()

    def load_bets(self):
        if not os.path.exists(BETS_FILE):
            return {}
        with open(BETS_FILE, "r") as f:
            return json.load(f)

    # Helper: Save bets
    def save_bets(self, bets):
        with open(BETS_FILE, "w") as f:
            json.dump(bets, f, indent=4)

    # @commands.command(name="xichun")
    # async def xichun(self, ctx, choice: str):
    #     choice = choice.lower()
    #     if choice.lower() not in ["die", "live"]:
    #         await ctx.send("Invalid choice. Use `?xichun die` or `?xichun live`.")
    #         return

    #     bets = self.load_bets()
    #     user_id = str(ctx.author.id)
    #     bets[user_id] = {
    #         "username": ctx.author.name,
    #         "bet": choice
    #     }
    #     self.save_bets(bets)

    #     await ctx.send(f"{ctx.author.name} placed a bet on **{choice.upper()}**! Vote now to win 100 fake coins!")

    @commands.command(name="xichun")
    async def xichun(self, ctx):
        bets = self.load_bets()
        user_id = str(ctx.author.id)

        if user_id not in bets:
            await ctx.send(f"{ctx.author.name}, you did not place a bet.")
            return

        bet = bets[user_id].get("bet", "???").upper()
        await ctx.send(f"{ctx.author.name}, your current bet is **{bet}**. All bets are closed.")

    def EnChapterNodeList_dict_generate(self):
        with open(f"./data/ENChapterNodeList.json", encoding="utf-8") as f:
            data = json.load(f)
        observe_num = []
        ids = []
        for d in data:
            observe_num.append(f"{d.get('chapterNumber')}-{d.get('node_index')} {d.get('chapter')} {d.get('title')} {d.get('stageDetail')}")
            ids.append(f"{d.get('story_theather_list_node_id')}_{d.get('node_index')}")
        return [ids,observe_num]

    def observation_dict_generate(self):
        observation_data = {}
        for file in os.listdir("./data/Limbus_Data"):
            if file.startswith("EN_AbnormalityGuides"):
                with open(f"./data/Limbus_Data/{file}", encoding="utf-8") as f:
                    data = json.load(f)
                    for dicts in data.get("dataList", []):
                        observation_data[dicts.get("id", 0)] = dicts
        observe_num = []
        for k, v in observation_data.items():
            observe_num.append((k, v.get("name", "") + " " + v.get("codeName", "")))
        return [observation_data.copy(), observe_num]
    
    def battlekeyword_dict_generate(self):
        battlekeyword_data = {}
        for file in os.listdir("./data/Limbus_Data"):
            if file.startswith("EN_BattleKeywords"):
                with open(f"./data/Limbus_Data/{file}", encoding="utf-8") as f:
                    data = json.load(f)
                    for dicts in data.get("dataList", []):
                        battlekeyword_data[dicts.get("id", "0")] = dicts
        battle_keyword_num = []
        for k, v in battlekeyword_data.items():
            battle_keyword_num.append((k, v.get("name", "")))
        return [battlekeyword_data.copy(), battle_keyword_num]

    def ego_gift_tier_generate(self):
        gift_data = {}
        for file in os.listdir("./data/Limbus_Data"):
            if file.startswith("ego-gift"):
                with open(f"./data/Limbus_Data/{file}", encoding="utf-8") as f:
                    data = json.load(f)
                    for dicts in data.get("list", []):
                        tag = dicts.get("tag","???")
                        if len(tag) == 1:
                            tag = tag[0].lower().capitalize().replace("_",": ")
                        gift_data[dicts.get("id", 0)] = tag
                        for upgrade in dicts.get("upgradeDataList",[]):
                            gift_data[upgrade.get("localizeID")] = tag

        return gift_data.copy()

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

    async def gift_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
     ):
        egos = self.gift_num
        return [
            discord.app_commands.Choice(name=ego[1], value=str(ego[0]))
            for ego in egos
            if current.lower() in ego[1].lower()
        ]

    async def observation_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ):
        egos = self.observation_num
        return [
            discord.app_commands.Choice(name=ego[1], value=str(ego[0]))
            for ego in egos
            if current.lower() in ego[1].lower()
        ]

    async def battlekeyword_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ):
        egos = self.battlekeyword_num
        return [
            discord.app_commands.Choice(name=ego[1], value=str(ego[0]))
            for ego in egos
            if current.lower() in ego[1].lower()
        ]

    async def en_chapter_node_list_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ):
        egos = self.en_chapter_node_list
        ego_pair = zip(egos[0], egos[1])
        return [
            discord.app_commands.Choice(name=ego[1][:100], value=ego[0])
            for ego in ego_pair
            if current.lower() in ego[1].lower()
        ]
    @app_commands.command()
    @app_commands.autocomplete(identities=identity_autocomplete)
    async def identity(
        self, interaction: discord.Interaction, identities: str, uptie_level: int = 4, private : bool = False
    ):
        """Limbus Identity Data"""
        data = await get_site_request_logged_in(
            f"https://malcute.aeonmoon.page/api/limbus2/identity_data/{identities}"
        )
        
        await identity_data_analysis(interaction, data, uptie_level, 45,private)

    @app_commands.command()
    @app_commands.autocomplete(ego=ego_autocomplete)
    async def ego_limbus(
        self, interaction: discord.Interaction, ego: str, uptie_level: int = 4,private: bool = False
    ):
        """Ego Limbus Data"""
        data = await get_site_request_logged_in(
            f"https://malcute.aeonmoon.page/api/limbus2/ego_data/{ego}"
        )
        await ego_data_analysis(interaction, data, uptie_level, private)

    @app_commands.command()
    @app_commands.autocomplete(gift=gift_autocomplete)
    async def gift_limbus(self, interaction: discord.Interaction, gift: str, private : bool = False):
        """Limbus Gift"""
        battleKeyWord = battle_keyword_dict()
        data = self.gift_data[int(gift)]
        embed = discord.Embed()
        embed.title = data.get("name", "")
        gift_id = data.get("id", 9744)
        tier = self.gift_tier_data.get(gift_id,"???")
        temp_description = f"""
{tier}
{data.get("desc", "")}
"""
        for word, en_name in battleKeyWord.items():
            temp_description = temp_description.replace(word, en_name)
        temp_description = re.sub("<[^>]+>", "**", temp_description)

        embed.description = temp_description
        temp_gift_id = gift
        file = None
        if os.path.exists(f"./data/limbus_images/gift_art/{temp_gift_id}.png"):
            image_path = f"./data/limbus_images/gift_art/{temp_gift_id}.png"
        elif len(temp_gift_id) > 4:
            temp_gift_id = temp_gift_id[1:]
            image_path = f"./data/limbus_images/gift_art/{temp_gift_id}.png"
        if os.path.exists(f"./data/limbus_images/gift_art/{temp_gift_id}.png"):
            embed.set_image(url="attachment://image.png")
            file = discord.File(image_path, filename="image.png")
        view = DeleteEmbedView(interaction.user, interaction.message)
        await interaction.response.defer(ephemeral=private)
        if file:
            await interaction.followup.send(embed=embed, file=file, view=view,ephemeral=private)
        else:
            await interaction.followup.send(embed=embed, view=view, ephemeral=private)

    @app_commands.command()
    @app_commands.autocomplete(observation=observation_autocomplete)
    async def observation_limbus(
        self, interaction: discord.Interaction, observation: str, private : bool = False
    ):
        """Abnormality Observations from Limbus"""
        data = self.observation_data[int(observation)]
        embed = discord.Embed()
        embed.title = data.get("name", "")
        desc = data.get("desc", "")
        clue = data.get("clue", "")
        obs = []
        for stories in data.get("storyList", []):
            obs.append("\n**" + str(stories.get("level", "0")) + "**")
            obs.append(stories.get("story", ""))
        obs = "\n".join(obs)
        description = f"""Desc: {desc}
Clue: {clue}
{obs}
"""
        if len(description) > 4095:
            description = description[:4096]
        description = re.sub("<[^>]+>", "**", description)
        embed.description = description
        file = None
        if os.path.exists(f"./data/limbus_images/portraits/{observation}_portrait.png"):
            image_path = f"./data/limbus_images/portraits/{observation}_portrait.png"
            embed.set_image(url="attachment://image.png")
            file = discord.File(image_path, filename="image.png")
        view = DeleteEmbedView(interaction.user, interaction.message)
        await interaction.response.defer(ephemeral=private)
        if file:
            await interaction.followup.send(embed=embed, file=file, view=view, ephemeral=private)
        else:
            await interaction.followup.send(embed=embed, view=view, ephemeral=private)

    @app_commands.command()
    @app_commands.autocomplete(battle_keyword=battlekeyword_autocomplete)
    async def keyword_limbus(
        self, interaction: discord.Interaction, battle_keyword: str,private : bool= False
    ):
        """Abnormality Observations from Limbus"""

        data = self.battlekeyword_data.get(battle_keyword)
        embed = discord.Embed()
        embed.title = data.get("name", "")
        desc = data.get("desc", "")
        description = f"""{desc}"""
        if len(description) > 4095:
            description = description[:4096]
        description = re.sub("<[^>]+>", "**", description)
        embed.description = description
        file = None
        # if os.path.exists(f"./data/limbus_images/portraits/{observation}_portrait.png"):
        #     image_path = f"./data/limbus_images/portraits/{observation}_portrait.png"
        #     embed.set_image(url="attachment://image.png")
        #     file = discord.File(image_path, filename="image.png")
        view = DeleteEmbedView(interaction.user, interaction.message)
        await interaction.response.defer(ephemeral=private)
        if file:
            await interaction.followup.send(embed=embed, file=file, view=view, ephemeral=private)
        else:
            await interaction.followup.send(embed=embed, view=view, ephemeral=private)

    @app_commands.command()
    async def emote_test(self,interaction: discord.Interaction):
        await interaction.response.send_message("<:limbusheads:1280657716871692472>")

    @app_commands.command()
    async def quote_limbus(self, interaction: discord.Interaction, arx: str):
        data = await get_site_post_logged_in(
            f"https://malcute.aeonmoon.page/api/limbus2/story", {"search":arx}
        )
        if data == "No Data Found":
            await interaction.response.send_message("Search parameters too generic or does not exist. (Message will self destruct)",delete_after=6)
            return
        data = json.loads(data)
        teller = '???'  # Default to unknown speaker
        if data.get('teller',False):
            title = data.get('title', '???')
            teller_name = data.get('teller', '???')
            teller = f"{title} - {teller_name}".strip() if title else teller_name
        elif data.get('model',False):
            # Fallback to model information if no teller
            name = data['model'].get('enname', '')
            nickName = data['model'].get('enNickName', '')
            teller = f"{nickName} - {name}".strip() if nickName else name


        author = arx
        description = f"""
Chapter: {data.get('chapter_info','???')}
Stage:{data.get('stage_info','???')}
Stage Num: {data.get('stage_id','???')}
Place:{data.get('stage_place','???')}
Dialouge #{data.get('id_raw','???')}
Speaker: {teller}
----------Content-----------
{data.get('content','-')}
"""
        embed = discord.Embed()
        embed.set_author(name=author)
        embed.description = description
        delete_button = DeleteEmbedView(author=interaction.user)
        await interaction.response.send_message(
            embed=embed,
            view=delete_button,
        )

    @app_commands.command()
    @app_commands.autocomplete(stage_name=en_chapter_node_list_autocomplete)
    async def limbus_story_search(
        self, interaction: discord.Interaction, stage_name: str,private : bool= False
    ):
        """Abnormality Observations from Limbus"""
        stage_parts = stage_name.split("_")
        node_id = int(stage_parts[0])
        node_index = int(stage_parts[1])
        data = await get_site_post_logged_in(
            f"https://malcute.aeonmoon.page/api/limbus2/story_query", {"node_id":node_id, "node_index":node_index}
        )
        chapter_id, chapter_observe_num = self.en_chapter_node_list
        final_stage_name = "Unknown"
        for i in range(0,len(chapter_observe_num)):
            if chapter_observe_num[i] == stage_name:
                final_stage_name = chapter_id[i]
        await story_data_display(interaction,final_stage_name,data,0,private=private)

    @commands.command()
    async def gacha(self,ctx):
        message = await ctx.send("Currently wrangling the chains of mirrors...")

        # Load the Twitter links JSON
        with open("./data/Twitter_links.json", encoding="utf-8") as f:
            twitter_dict = json.load(f)

        # Get the gacha data
        data = await get_site_content_json("https://malcute.aeonmoon.page/api/limbus2/gacha")
        
        # Generate the image
        image_bytes = await self.stitch_images(data)

        # If "Special", send random Twitter link first
        if image_bytes == "Special":
            random_pick = random.choice(twitter_dict)
            await message.edit(content=f"{random_pick['title']} \n\n{random_pick['link']}")
        
        # Prepare the image file
        file = discord.File(image_bytes, filename="stitched_image.png")
        embed = discord.Embed(title="Stitched Image", description="Here is the generated image grid:")
        embed.set_image(url="attachment://stitched_image.png")

        # Send the embed separately with the image
        await ctx.send(embed=embed, file=file)


    def crop_image(self,img):
        width, height = img.size
        left = width // 4
        right = width - (width // 4)
        img = img.crop((left, 0, right, height))
        return img

    def enhance_image(self,img, rank):
        if rank in [3, "EGO"]:
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(1.5)  # Make it shinier
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.3)
        return img
    
    async def fetch_image(self, session, img_url):
        async with session.get(img_url) as response:
            return await response.read()

    async def stitch_images(self,image_list, final_width=1521, final_height=856):
        cols, rows = 5, 2  # 5 images per row, 2 rows
        thumb_width, thumb_height = final_width // cols, final_height // rows
        
        images = []
        base_url = f"{LINK}/django_static/Limbus_Data/"  # Example base URL
        
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_image(session, f"{base_url}{item['id']}.jpg") for item in image_list]
            responses = await asyncio.gather(*tasks)

        for item in image_list:
            if(item['rank'] == "Special"):
                return "Special"
            if(item['rank'] != "Ego"):
                img_url = f"{base_url}full_art/{item['id']}_normal.png"
            else:
                img_url = f"{base_url}ego_art/{item['id']}_cg.png"
            rank = item['rank']
            response = requests.get(img_url)
            img = Image.open(BytesIO(response.content))
            img = self.crop_image(img)
            img = img.resize((thumb_width, thumb_height), Image.ANTIALIAS)
            img = self.enhance_image(img, rank)
            images.append(img)
        
        # Create a blank final image
        final_image = Image.new("RGB", (final_width, final_height))
        
        # Paste images into grid
        for index, img in enumerate(images):
            x_offset = (index % cols) * thumb_width
            y_offset = (index // cols) * thumb_height
            final_image.paste(img, (x_offset, y_offset))
        
            # Convert to bytes for Discord
        img_bytes = BytesIO()
        final_image.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        return img_bytes



    # @app_commands.command()
    # @app_commands.autocomplete(stage_name=en_chapter_node_list_autocomplete)
    # async def story_search_by_node(
    #     self, interaction: discord.Interaction, stage_name: str,private : bool= False
    # ):
    #     """Abnormality Observations from Limbus"""
    #     stage_parts = stage_name.split("_")
    #     node_id = int(stage_parts[0])
    #     node_index = int(stage_parts[1])
    #     data = await get_site_post_logged_in(
    #         f"https://malcute.aeonmoon.page/api/limbus2/story_query", {"node_id":node_id, "node_index":node_index}
    #     )
    #     await story_data_display(interaction,"test_chapter",data,0,private=private)
# AbnormalitiesGuide
# EN_EGOgift_mirrordungeon
# Need gift images
# need abno images


async def setup(bot):
    await bot.add_cog(Limbus(bot))
