from discord.ext import commands
import discord
from utils.cardScrape import (
    get_site_content,
    make_into_string,
    scrape_deck_image,
    get_site_content_json,
)
import pandas as pd
import os

LINK = "http://aeonmoon.herokuapp.com"


class searchCard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ssearch(self, ctx, *, arx: str):
        soup = await get_site_content(f"{LINK}/lor/card/")
        soup = soup.find_all("li")
        list_of_card = []
        found = False
        for cards in soup:
            if str(arx).lower() == cards.get_text().lower():
                link = cards.find("a").get("href")
                found = True
                link = f"{LINK}{link}"
                temp_soup = await get_site_content(link)
                kek = temp_soup.find_all("img")[1].get("src")
                kek = kek.replace(" ", "%20")
                img = f"http://aeonmoon.herokuapp.com{kek}"
                tables = pd.read_html(link)
                datas = make_into_string(tables)
                embed = discord.Embed()
                embed.color = 3066993
                embed.set_author(name=str(arx))
                embed.description = datas[0]
                embed.add_field(name="Dice Rolls", value=datas[1], inline=True)
                embed.add_field(name="Dice Effects", value=datas[2], inline=True)
                embed.add_field(name="Dice Type", value=datas[3], inline=True)
                embed.set_image(url=img)
                embed.add_field(
                    name="Visit this card's website",
                    value=link,
                    inline=False,
                )

                await ctx.send(embed=embed)
            elif str(arx).lower()[0] == cards.get_text().lower()[0]:
                list_of_card.append(cards.get_text().lower())

        if not found:
            mewembed = discord.Embed()
            mewembed.color = 3066993
            mewembed.set_author(name=f"We couldn't find {str(arx)}, Did you mean: \n")
            stuff = ""
            for cards in list_of_card:
                stuff += f"{cards}\n"
            mewembed.description = stuff
            await ctx.send(embed=mewembed)

    @commands.command()
    async def search(self, ctx, *, arx: str):
        soup = await get_site_content(f"{LINK}/lor/card/")
        soup = soup.find_all("li")
        list_of_card = []
        found = False
        for cards in soup:
            if str(arx).lower() == cards.get_text().lower():
                link = cards.find("a").get("href")
                found = True
                link = f"{LINK}{link}"
                temp_soup = await get_site_content(link)
                kek = temp_soup.find_all("img")[1].get("src")
                kek = kek.replace(" ", "%20")
                img = f"http://aeonmoon.herokuapp.com{kek}"
                tables = pd.read_html(link)
                datas = make_into_string(tables)
                embed = discord.Embed()
                embed.color = 3066993
                embed.set_author(name=str(arx))
                embed.description = datas[0]
                embed.add_field(name="Dice Rolls", value=datas[1], inline=True)
                embed.add_field(name="Dice Type", value=datas[2], inline=True)
                embed.add_field(name="Dice Effects", value=datas[3], inline=True)
                embed.set_image(url=img)
                embed.add_field(
                    name="Visit this card's website",
                    value=link,
                    inline=False,
                )

                await ctx.send(embed=embed)
            elif str(arx).lower()[0] == cards.get_text().lower()[0]:
                list_of_card.append(cards.get_text().lower())

        if not found:
            mewembed = discord.Embed()
            mewembed.color = 3066993
            mewembed.set_author(name=f"We couldn't find {str(arx)}, Did you mean: \n")
            stuff = ""
            for cards in list_of_card:
                stuff += f"{cards}\n"
            mewembed.description = stuff
            await ctx.send(embed=mewembed)

    @commands.command()
    async def sdeck(self, ctx, arx: int):
        soup = await get_site_content_json(f"{LINK}/lor/api/deck/{arx}?format=json")
        name = soup["name"]
        creator = soup["creator"]
        recc_floor = soup["Recc_Floor"]
        recc_page = soup["Recc_Page"]
        recc_rank = soup["Recc_Rank"]
        general_info_str = f"""
        > Creator: {creator}
        > Recommended Floor: {recc_floor}
        > Recommended Page: {recc_page}
        > Recommended Rank: {recc_rank}
        > Make Your deck: http://aeonmoon.herokuapp.com/lor/deck/add/"""
        eff = soup["effect"]
        effstr = ""
        for effs in eff:
            effstr += f"> {effs}\n"
        cardstr = ""

        for card in soup["card_count"]:
            cardstr += f"> {card['card_id']} x{card['card_count']}\n"
        list_of_img = []
        list_of_name = []
        cards = soup["cards"]
        for img in cards:
            kek = img["ImgPath"]
            list_of_name.append(img["Name"])
            kek = kek.replace(" ", "%20")
            list_of_img.append(f"http://aeonmoon.herokuapp.com/static/{kek}")

        true_list_img = []
        for imglink, name in zip(list_of_img, list_of_name):
            for shits in soup["card_count"]:
                if name == shits["card_id"]:
                    for i in range(shits["card_count"]):
                        true_list_img.append(imglink)
        finalImg = await scrape_deck_image(true_list_img)
        finalImg.save("tmp/tmp.png")
        file = discord.File("tmp/tmp.png", filename="image.png")
        embed = discord.Embed()
        embed.color = 3447003
        embed.set_author(name=name)
        embed.description = general_info_str
        if effstr != "":
            embed.add_field(name="Page Effects", value=effstr)
        embed.add_field(name="Cards", value=cardstr)
        embed.set_footer(text=f"{LINK}/lor/deck/{int(arx)}")
        embed.set_image(url="attachment://image.png")
        return await ctx.send(file=file, embed=embed)
        os.remove("tmp/tmp.png")


def setup(bot):
    bot.add_cog(searchCard(bot))
