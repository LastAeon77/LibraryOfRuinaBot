from discord.ext import commands, tasks
import discord
from datetime import datetime
from rapidfuzz import fuzz, process

# import tweepy
from googleapiclient.discovery import build
import matplotlib.pyplot as plt
import matplotlib.dates
from utils.cardScrape import (
    get_site_content_json,
)

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
        self.printer.start()
        self.below_150000 = True

    async def fuzzy_search(self,query,choices):
        best_match = process.extractOne(query.lower(),choices,processor=None,scorer=fuzz.ratio)
        best_match = best_match[0]
        best_match = best_match.split("|")
        return best_match

    @commands.hybrid_command()
    async def count(self, ctx):
        """Prints out the number of youtube and twitter follower count"""
        twitter_count = await self.get_twitter_user()
        youtube_sub = await self.get_youtube_sub()
        total = int(youtube_sub) + int(twitter_count)
        embed = discord.Embed()
        embed.set_author(name="ProjectMoon Limbus Follower Total")
        embed.description = f"""
        Youtube Subscribers: {youtube_sub}
        Limbus Twitter Followers: {twitter_count} (API no longer available)
        Total: {total}
        """
        with open(FILE_NAME_TWITTER, "a") as f:
            f.write(f"\n{twitter_count}")
        with open(FILE_NAME_YOUTUBE, "a") as f:
            f.write(f"\n{youtube_sub}")
        with open(FILE_NAME_TIME, "a") as f:
            f.write(f"\n{datetime.now()}")
        await ctx.send(embed=embed)

        return [int(twitter_count), int(youtube_sub)]

    async def get_twitter_user(self):
        # consumer_key = self.bot.config["twitter"]["API key"]
        # consumer_secret = self.bot.config["twitter"]["API secret key"]
        # access_token = self.bot.config["twitter"]["Access-token"]
        # access_token_secret = self.bot.config["twitter"]["Access-Secret-Token"]
        # auth = tweepy.OAuth1UserHandler(
        #     consumer_key, consumer_secret, access_token, access_token_secret
        # )
        # api = tweepy.API(auth)
        # twitter_user_count = api.get_user(screen_name="LimbusCompany_B")
        # twitter_user_count = twitter_user_count.followers_count
        # return int(twitter_user_count)
        # due to new twitter policy of destroying API
        return 0

    async def get_youtube_sub(self):
        youtube_API_key = self.bot.config["youtube"]["API key"]
        youtube = build("youtube", "v3", developerKey=youtube_API_key)

        ch_request = youtube.channels().list(
            part="statistics", id="UCpqyr6h4RCXCEswHlkSjykA"
        )
        ch_response = ch_request.execute()
        sub = ch_response["items"][0]["statistics"]["subscriberCount"]
        return int(sub)

    @tasks.loop(minutes=30.0)
    async def printer(self):
        twitter_count = await self.get_twitter_user()
        youtube_sub = await self.get_youtube_sub()
        with open(FILE_NAME_TWITTER, "a") as f:
            f.write(f"\n{twitter_count}")
        with open(FILE_NAME_YOUTUBE, "a") as f:
            f.write(f"\n{youtube_sub}")
        with open(FILE_NAME_TIME, "a") as f:
            f.write(f"\n{datetime.now()}")

    async def growth(self, ctx, hours=8):
        with open(FILE_NAME_TWITTER, "r") as f:
            twitter_counts = list(map(int, f.read().split("\n")))
        with open(FILE_NAME_YOUTUBE, "r") as f:
            youtube_counts = list(map(int, f.read().split("\n")))
        with open(FILE_NAME_TIME, "r") as f:
            dates = f.read().split("\n")
        datetime_dates = [datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f") for x in dates]
        # dates = matplotlib.dates.date2num(datetime_dates)
        total_count = []
        for t, y in zip(twitter_counts, youtube_counts):
            total_count.append(t + y)
        #########
        y_p = []
        x_p = []
        current_delta = 0
        step = 0
        for i in range(40, len(total_count)):
            time_delta = datetime_dates[i] - datetime_dates[i - 1]
            total_seconds = time_delta.total_seconds()
            current_delta += total_seconds
            step += 1
            if current_delta >= (60 * 60 * (hours - 1)):
                # time_in_between = datetime_dates[i] - timedelta(
                #     minutes=int(current_delta / 2)
                # )
                y_p.append((total_count[i] - total_count[i - step]))
                x_p.append(datetime_dates[i])
                current_delta = 0
                step = 0
            elif current_delta > 60 * 60 * (hours + 1):
                current_delta = 0
                step = 0
        ##########

        plt.figure(facecolor="#36393e")
        ax = plt.axes()
        ax.set_facecolor("#36393e")
        ax.get_yaxis().get_major_formatter().set_useOffset(False)
        ax.get_yaxis().get_major_formatter().set_scientific(False)
        plt.title("Growth Rate", color="white")
        plt.xlabel("Date", fontweight="bold", color="white", fontsize=12)
        plt.ylabel(
            f"Follower Increase Rate every {hours} hours",
            fontweight="bold",
        )
        plt.xticks(color="white")
        plt.yticks(color="white")
        plt.grid(True)
        plt.plot(x_p, y_p, "r", linestyle="solid")
        plt.tight_layout()
        plt.gcf().set_size_inches(10, 5.5)
        plt.savefig(IMAGE_LOCATION, dpi=100)
        with open(IMAGE_LOCATION, "rb") as f:
            await ctx.send(content=None, file=discord.File(f))
        plt.close()

    async def make_normal_graph(self, ctx):
        goals = [
            100000,
            120000,
            130000,
            150000,
            180000,
            210000,
            240000,
            270000,
            300000,
            1000000,
        ]
        with open(FILE_NAME_TWITTER, "r") as f:
            twitter_counts = list(map(int, f.read().split("\n")))
        with open(FILE_NAME_YOUTUBE, "r") as f:
            youtube_counts = list(map(int, f.read().split("\n")))
        with open(FILE_NAME_TIME, "r") as f:
            dates = f.read().split("\n")
        datetime_dates = [datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f") for x in dates]
        total_count = []
        for t, y in zip(twitter_counts, youtube_counts):
            total_count.append(t + y)
        # get nearest goal
        goal = 100000
        for g in goals:
            if total_count[-1] < g:
                goal = g
                break
        dates = matplotlib.dates.date2num(datetime_dates)
        plt.figure(facecolor="#36393e")
        ax = plt.axes()
        ax.set_facecolor("#36393e")
        ax.get_yaxis().get_major_formatter().set_useOffset(False)
        ax.get_yaxis().get_major_formatter().set_scientific(False)
        # ax.xaxis.set_major_locator(matplotlib.dates.WeekdayLocator(byweekday=FR))
        plt.title("Total Follower Count over time", color="white")
        plt.xlabel("Date", fontweight="bold", color="white", fontsize=12)
        plt.ylabel("Total Follower", fontweight="bold", color="white")
        plt.xticks(color="white")
        plt.yticks(color="white")
        plt.ylim([twitter_counts[0] + youtube_counts[0], goal])
        plt.grid(True)
        plt.plot_date(dates, total_count, "r", linestyle="solid")
        plt.tight_layout()
        plt.gcf().set_size_inches(10, 5.5)
        plt.savefig(IMAGE_LOCATION, dpi=100)
        with open(IMAGE_LOCATION, "rb") as f:
            await ctx.send(content=None, file=discord.File(f))
        plt.close()

    @commands.hybrid_command()
    async def graph(self, ctx, arx=None, arx2=None):
        """?graph <optional: growth> for follower count"""
        if arx is None:
            await self.make_normal_graph(ctx)
        elif arx == "growth" and arx2 is None:
            await self.growth(ctx)
        elif arx == "growth" and arx2.isdecimal():
            await self.growth(ctx, float(arx2))
        else:
            await ctx.send("Error")

    @commands.hybrid_command()
    async def iden(self, ctx, *, arx: str):
        """Shows identity info"""
        await self.identity(ctx, arx=arx)

    @commands.hybrid_command()
    async def identity(self, ctx, *, arx: str):
        """Shows identity info"""
        color_code = {3: 0xF1C40F, 2: 0xE74C3C, 1: 0x979C9F}
        message = await ctx.send("Loading...")
        soup = await get_site_content_json(f"{LINK}/api/limbus/identity")
        choices = []
        for x in soup:
            choices.append(f"{x['name'].lower()}|{x['sinner'].lower()}")
        best_match = await self.fuzzy_search(arx.lower(),choices=choices)
        sinner = best_match[1]
        best_match = best_match[0]
        true_identity = [
            x
            for x in soup
            if x["name"].lower() == best_match.strip()
            and x["sinner"].lower() == sinner.strip()
        ]
        true_identity = true_identity[0]
        embed = discord.Embed()
        embed.set_author(name=true_identity["name"])

        general_info_string = f"""
HP: {str(true_identity['hp'])}
Block:{str(true_identity['block'])}
Speed:{str(true_identity['speed'])}
Growth: {true_identity['growth']}
Rarity : {"".join(["0" for i in range(true_identity['rarity'])])}
        """

        embed.add_field(name="General Info", value=general_info_string)
        embed.add_field(name="Affinity", value=true_identity["affinity"])
        embed.add_field(name="Sinner", value=true_identity["sinner"])
        passive_string = f"""
Combat= {true_identity["passive_on_field"]}
Support= {true_identity["passive_off_field"]}        
        """
        embed.add_field(name="Passives", value=passive_string)

        skill_string = f"""
Skill 1: {true_identity['skill_1']} x{true_identity['skill_1_count']}
Skill 2: {true_identity['skill_2']} x{true_identity['skill_2_count']}
Skill 3: {true_identity['skill_3']} x{true_identity['skill_3_count']}
        """
        resist_string = f"""
Reist Slash: {true_identity['resistance_slash']}
Resist Pierce: {true_identity['resistance_pierce']}
Resist Blunt: {true_identity['resistance_blunt']}
        """
        embed.add_field(name="Skills", value=skill_string)
        embed.add_field(name="Resists", value=resist_string)
        imgpath = (
            true_identity["image_link"]
            if true_identity["image_link"] and len(true_identity["image_link"]) > 0
            else "https://cdn.discordapp.com/attachments/750725415391330378/1079440000371937391/image.png"
        )

        embed.set_image(url=imgpath)
        embed.color = color_code[true_identity["rarity"]]
        delete_button = DeleteEmbedView(author=ctx.author, message=message)
        await message.edit(
            content="",
            embed=embed,
            view=delete_button,
        )

    @commands.hybrid_command()
    async def ego(self, ctx, *, arx: str):
        """Shows Limbus EGO info"""
        RESISTANCE_LIST = [
            "resistance_wrath",
            "resistance_lust",
            "resistance_sloth",
            "resistance_gluttony",
            "resistance_gloom",
            "resistance_pride",
            "resistance_envy",
        ]
        message = await ctx.send("Loading...")
        soup = await get_site_content_json(f"{LINK}/api/limbus/EGO")
        choices = []
        for x in soup:
            choices.append(f"{x['name'].lower()}|{x['sinner'].lower()}")
        # best_match = process.extractOne(arx.lower(), choices, scorer=fuzz.ratio)
        # best_match = best_match[0]
        # best_match = best_match.split("|")
        best_match = await self.fuzzy_search(arx.lower(),choices=choices)
        sinner_name = best_match[1]
        name = best_match[0]
        true_identity = [
            x
            for x in soup
            if x["name"].lower() == name and x["sinner"].lower() == sinner_name
        ]
        true_identity = true_identity[0]
        embed = discord.Embed()
        embed.set_author(name=true_identity["name"])
        # embed.add_field(
        #     name="Rarity",
        #     value=("".join(["0" for i in range(true_identity["rarity"])])),
        # )
        embed.add_field(name="Sinner", value=true_identity["sinner"])
        embed.add_field(
            name="Passive on Field", value=true_identity["passive_on_field"]
        )
        # embed.add_field(
        #     name="Passive off Field", value=true_identity["passive_off_field"]
        # )
        # embed.add_field(name="Skills", value=true_identity["skills"])
        embed.add_field(name="Awakening Skill", value=true_identity["awakening_skill"])
        embed.add_field(name="Corrision Skill", value=true_identity["corrision_skill"])
        for resist in RESISTANCE_LIST:
            if true_identity[resist] != "Normal":
                new_string = "Resist " + resist.split("_")[1].capitalize()
                embed.add_field(name=new_string, value=true_identity[resist])
        imgpath = (
            true_identity["image_link"]
            if true_identity["image_link"] and len(true_identity["image_link"]) > 0
            else "https://cdn.discordapp.com/attachments/750725415391330378/1079440000371937391/image.png"
        )

        embed.set_image(url=imgpath)
        delete_button = DeleteEmbedView(author=ctx.author, message=message)
        await message.edit(
            content="",
            embed=embed,
            view=delete_button,
        )

    @commands.hybrid_command()
    async def passive(self, ctx, *, arx: str):
        message = await ctx.send("Loading...")
        soup = await get_site_content_json(f"{LINK}/api/limbus/passive")
        soup_2 = await get_site_content_json(f"{LINK}/api/limbus/passive_ego")
        soup = soup + soup_2
        choices = []
        for x in soup:
            choices.append(f"{x['name'].lower()}")
        best_match = process.extractOne(arx.lower(), choices, scorer=fuzz.ratio)
        best_match = best_match[0]
        true_match = [x for x in soup if x["name"].lower() == best_match]
        true_match = true_match[0]
        embed = discord.Embed()
        embed.set_author(name=true_match["name"])
        embed.add_field(name="Description", value=true_match["desc"])
        await message.edit(
            content="",
            embed=embed,
        )

    @commands.hybrid_command()
    async def skill(self, ctx, *, arx: str):
        color_code = {
            "Wrath": 0x992D22,
            "Lust": 0xA84300,
            "Sloth": 0xF1C40F,
            "Gluttony": 0x2ECC71,
            "Gloom": 0x3498DB,
            "Pride": 0x206694,
            "Envy": 0x71368A,
        }
        message = await ctx.send("Loading...")
        soup = await get_site_content_json(f"{LINK}/api/limbus/skill")
        soup_2 = await get_site_content_json(f"{LINK}/api/limbus/skill_ego")
        soup = soup + soup_2
        choices = []
        for x in soup:
            choices.append(f"{x['name'].lower()}| {x['level']}|{x['in_game_id']}|{x.get('emotion_type','')}")
        best_match = await self.fuzzy_search(arx.lower(),choices=choices)
        name = best_match[0]
        level = int(best_match[1])
        in_game_id = best_match[2]
        emotion_type = best_match[3]

        true_match = [
            x
            for x in soup
            if x["name"].lower() == name
            and int(x["level"]) == int(level)
            and x["in_game_id"] == in_game_id
            and x.get('emotion_type','') == emotion_type
        ]
        true_match = true_match[0]
        embed = discord.Embed()
        embed.set_author(
            name=f"{true_match.get('name','none')} {true_match.get('in_game_id','')}"
        )
        general_info = f"""Level: {true_match.get('level','')}
Sin Type: {true_match.get('type','')}
Damage Type: {true_match.get('damage_type','-')}
        """
        if true_match.get('emotion_type'):
            general_info += f"Emotion Type: {true_match.get('emotion_type')}"
        embed.add_field(name="General Info", value=general_info, inline=False)

        embed.add_field(name="Effect", value=true_match.get("desc", ""), inline=False)
        coin_effects = true_match.get("coindescs", "").split("\n")
        coin_effects_string = f"{str(true_match.get('coin_roll',0))} \n"
        if true_match.get("coin_num") and true_match.get('coin_mod'):
            for i in range(true_match.get("coin_num", 0)):
                coin_effects_string += f"{('+'+ str(true_match.get('coin_mod',0))) if int(true_match.get('coin_mod'))>0 else true_match.get('coin_mod',0) }: {coin_effects[i] if i<len(coin_effects) else ''}\n"
        embed.color = color_code.get(true_match.get("type", "fgds"), 0x71368A)
        embed.add_field(name="Rolls", value=coin_effects_string, inline=False)
        await message.edit(
            content="",
            embed=embed,
        )

    @commands.hybrid_command()
    async def key(self, ctx, *, arx: str):
        message = await ctx.send("Loading...")
        soup = await get_site_content_json(f"{LINK}/api/limbus/battle_keyword")
        choices = []
        for x in soup:
            choices.append(f"{x['name'].lower()}")
        best_match = process.extractOne(
            arx.lower(), choices, processor=None, scorer=fuzz.ratio
        )
        best_match = best_match[0]
        true_match = [x for x in soup if x["name"].lower() == best_match]
        true_match = true_match[0]
        embed = discord.Embed()
        embed.set_author(name=true_match["name"])
        embed.add_field(name="Description", value=true_match["desc"], inline=False)
        await message.edit(
            content="",
            embed=embed,
        )


async def setup(bot):
    await bot.add_cog(Limbus(bot))
