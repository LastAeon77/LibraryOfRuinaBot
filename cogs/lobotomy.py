from discord.ext import commands
import discord
from rapidfuzz import fuzz, process
import json

# import tweepy
from utils.cardScrape import (
    get_site_content_json,
)

LINK = "https://malcute.aeonmoon.page"


class Lobotomy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def lcabno(self, ctx, *, arx: str):
        message = await ctx.send("Loading...")
        # soup = await get_site_content_json(f"{LINK}/asp/api/Abnormalities")
        with open("./data/abno_data.json", "r", encoding="cp866") as abno_data:
            soup = json.loads(abno_data.read())
        choices = []
        for x in soup:
            choices.append(f"{x['name'].lower()}")
            choices.append(f"{x['numCode'].lower()}")
        best_match = process.extractOne(arx.lower(), choices, scorer=fuzz.ratio)
        print(best_match)
        best_match = best_match[0]
        for x in soup:
            if x["name"].lower() == best_match or x["numCode"].lower() == best_match:
                true_match = x
        embed = discord.Embed()

        embed.set_author(name=true_match["name"])
        embed.description = f"{true_match['openText']}"
        embed.add_field(name="Code number", value=true_match["numCode"])
        embed.add_field(name="Risk Level", value=true_match["riskLevel"])
        embed.add_field(name="Box Thread", value=true_match["openText"])

        tip_string = ""
        for i, tip in enumerate(true_match["tips"]):
            tip_string += f"{i+1}: {tip['tip'][:30]}\n"
        story_string = ""
        for story in true_match["stories"]:
            story_string += f"{story['storyNumb']}: {story['story'][:20]}...\n"
        narration_string = ""
        for narration in true_match["narrations"]:
            narration_string += (
                f"{narration['narrationAction']}: {narration['narration']}\n"
            )

        embed.add_field(name="Tips", value=tip_string)
        embed.add_field(name="Story", value=story_string)
        # embed.add_field(name="Narration", value=narration_string)
        color_code = {
            "ZAYIN": 0x57F287,
            "TETH": 0x3498DB,
            "HE": 0xFFFF00,
            "WAW": 0x9B59B6,
            "ALEPH": 0xED4245,
        }
        embed.color = color_code.get(true_match["riskLevel"], 0x57F287)
        await message.edit(
            content="",
            embed=embed,
        )


async def setup(bot):
    await bot.add_cog(Lobotomy(bot))
