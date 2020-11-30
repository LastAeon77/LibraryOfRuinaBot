from discord.ext import commands
import discord
from utils.cardScrape import (
    get_site_content,
    make_into_string,
    scrape_deck_image,
    get_image_content,
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
    async def sdeck(self, ctx, arx: int):
        soup = await get_site_content(f"{LINK}/lor/deck/{arx}")
        name = soup.find("h1")
        ps = soup.find_all("p")
        creator = ps[0].get_text()
        avg_cost = ps[1].get_text()
        recc_floor = ps[2].get_text()
        recc_page = ps[3].get_text()
        general_info_str = f"""
        > {creator}
        > {avg_cost}
        > {recc_floor}
        > {recc_page}
        > Make Your deck: http://aeonmoon.herokuapp.com/lor/deck/add/"""
        eff = soup.find_all("li", {"class": "has-text-primary"})
        effstr = ""
        for effs in eff:
            effstr += f"> {effs.get_text().split(':')[0]}\n"
        cards = soup.find_all("li", {"class": ""})
        cardstr = ""
        for card in cards:
            cardstr += f"> {card.get_text()}\n"
        imgs = soup.find_all("img")
        imgs = imgs[1:]
        list_of_img = []
        for img in imgs:
            kek = img.get("src")
            kek = kek.replace(" ", "%20")
            list_of_img.append(f"http://aeonmoon.herokuapp.com{kek}")
        finalImg = await scrape_deck_image(list_of_img)
        finalImg.save("tmp/tmp.png")
        file = discord.File("tmp/tmp.png", filename="image.png")
        embed = discord.Embed()
        embed.color = 3447003
        embed.set_author(name=name.get_text())
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
