from discord.ext import commands
from rapidfuzz import fuzz, process
import discord
from utils.cardScrape import (
    scrape_deck_image,
    get_site_content_json,
)

LINK = "https://malcute.aeonmoon.page"
FILE_NAME = "./data/allowed_channels.txt"

color_dict = {
    "Paperback": 0x2ECC71,
    "Hardcover": 0x3498DB,
    "Limited": 0x9B59B6,
    "Objet d'art": 0xF1C40F,
    "EGO": 0xE74C3C,
}
Rarity_dict = {
    "P": "Paperback",
    "H": "Hardcover",
    "L": "Limited",
    "O": "Objet d'art",
    "E": "EGO",
}


class DeleteEmbedView(discord.ui.View):
    def __init__(self, author, message=None):
        super().__init__()
        self.author = author
        self.message = message

    @discord.ui.button(label="Delete", style=discord.ButtonStyle.red)
    async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user == self.author:
            await interaction.message.delete()


class searchCard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # for promun discord only
        with open(FILE_NAME, "r") as f:
            self.allowed_channel = list(map(int, f.read().split("\n")))

    async def get_allowed_channel(self):
        return str(self.allowed_channel)

    async def cardSearch(self, ctx, arx: str):
        message = await ctx.send("Loading...")
        soup = await get_site_content_json(f"{LINK}/api/lor/card")
        card_data = [x for x in soup if str(x["Name"]).lower() == str(arx).lower()]
        used_best_match = False
        if not card_data:
            choices = []
            for x in soup:
                choices.append(x["Name"].lower())
            best_match = process.extractOne(arx.lower(), choices, scorer=fuzz.ratio)
            best_match = best_match[0]
            card_data = [x for x in soup if x["Name"].lower() == best_match]
            used_best_match = True
        if card_data:
            data = card_data[0]
            name = data["Name"]
            link = f"https://aeonmoon.vercel.app/lor/card/{data['slug']}"
            imgpath = data["ImgPath"]
            if imgpath[:8] == "LoR_Data":
                imgpath = (
                    f"https://malcute.aeonmoon.page/django_static/{imgpath}".replace(
                        " ", "%20"
                    )
                )

            if data["On_Play_Effect"] == "NULL":
                data["On_Play_Effect"] = "-"
            # Make everything - when None
            for k, v in data.items():
                if not v:
                    data[k] = "-"
            embed = discord.Embed()
            embed.color = color_dict[data["Rarity"]]
            embed.set_author(name=name)
            embed.description = f"""
            Rank: {data['rank']}
            Guest: {data['office']}
            Rarity: {data['Rarity']}
            OnPlayEff: {data['On_Play_Effect']}
            Cost: {data['Cost']}
            Type: {data['CardType']}
                        """
            dice_rolls = f"""
            > {data['Roll1']}
            > {data['Roll2']}
            > {data['Roll3']}
            > {data['Roll4']}
            > {data['Roll5']}
            """
            embed.add_field(name="Dice Rolls", value=dice_rolls, inline=True)

            dice_effects = f"""
            > {data['Eff1']}
            > {data['Eff2']}
            > {data['Eff3']}
            > {data['Eff4']}
            > {data['Eff5']}
            """
            embed.add_field(name="Dice Effects", value=dice_effects, inline=True)
            dice_type = f"""
            > {data['Type1']}
            > {data['Type2']}
            > {data['Type3']}
            > {data['Type4']}
            > {data['Type5']}
            """
            embed.add_field(name="Dice Type", value=dice_type, inline=True)
            embed.set_image(url=imgpath)
            embed.add_field(
                name="Visit this card's website",
                value=link,
                inline=False,
            )
            delete_button = DeleteEmbedView(author=ctx.author, message=message)
            if used_best_match:
                await message.edit(
                    content="Card not found! Here is the best match",
                    embed=embed,
                    view=delete_button,
                )
            else:
                await message.edit(embed=embed, view=delete_button)

    @commands.hybrid_command()
    async def search(self, ctx, *, arx: str):
        """?search <cardname> searches for best match card name"""
        if ctx.message.guild.id != 718294958573879347:
            await self.cardSearch(ctx, arx)

        else:
            if ctx.message.channel.id in self.allowed_channel:
                await self.cardSearch(ctx, arx)
            else:
                await ctx.send("This command is not allowed in this channel.")

    @commands.command()
    async def allow_channel(self, ctx, arx: int):
        """Allows certain channels to be able to use a ?search"""
        arx = int(arx)
        if ctx.message.author.id == self.bot.config["discord"]["owner"]:
            self.allowed_channel.append(arx)
            await ctx.send(f"Added channel {arx}")
        else:
            await ctx.send("You are not allowed to use this command")
        with open(FILE_NAME, "a") as f:
            f.write(f"\n{arx}")

    @commands.command()
    async def disallow_channel(self, ctx, arx: int):
        """disallow certain channels to be able to use a ?search"""
        arx = int(arx)
        if ctx.message.author.id == self.bot.config["discord"]["owner"]:
            self.allowed_channel.append(arx)
            await ctx.send(f"Removed channel {arx}")
        else:
            await ctx.send("You are not allowed to use this command")

    async def searchDeck(self, ctx, arx: str):
        data = await get_site_content_json(f"{LINK}/api/lor/deck?format=json")
        choices = []
        for x in data:
            choices.append(x["name"].lower())
        best_match = process.extractOne(arx.lower(), choices, scorer=fuzz.ratio)
        best_match = best_match[0]
        soup = [x for x in data if x["name"].lower() == best_match]
        soup = soup[0]
        name_of_deck = soup["name"]
        creator = soup["creator"]
        recc_floor = soup["Recc_Floor"]
        recc_page = soup["Recc_Page"]
        recc_rank = soup["Recc_Rank"]
        general_info_str = f"""
        > Creator: {creator}
        > Recommended Floor: {recc_floor}
        > Recommended Page: {recc_page}
        > Recommended Rank: {recc_rank}
        > Make Your deck: https://malcute.aeonmoon.page/lor/createdeck"""
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
            if kek[:8] == "LoR_Data":
                kek = kek.replace(" ", "%20")
                list_of_img.append(f"https://malcute.aeonmoon.page/django_static/{kek}")
            else:
                list_of_img.append(kek)

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
        embed.set_author(name=name_of_deck)
        embed.description = general_info_str
        if effstr != "":
            embed.add_field(name="Page Effects", value=effstr)
        embed.add_field(name="Cards", value=cardstr)
        embed.set_footer(text=f"https://malcute.aeonmoon.page/lor/deck/{str(soup['id'])}")
        embed.set_image(url="attachment://image.png")
        delete_button = DeleteEmbedView(author=ctx.author)
        return await ctx.send(file=file, embed=embed, view=delete_button, content="You can now make decks at `malcute.aeonmoon.page/lor/createdeck` (fixed)")

    @commands.command()
    async def deck(self, ctx, *, arx: str):
        """Looks for community made decks"""
        if ctx.message.guild.id != 718294958573879347:
            await self.searchDeck(ctx, arx)

        else:
            if ctx.message.channel.id in self.allowed_channel:
                await self.searchDeck(ctx, arx)
            else:
                await ctx.send("This command is not allowed in this channel.")

    async def searchAbno(self, ctx, search: str):
        message = await ctx.send("Loading...")
        delete_button = DeleteEmbedView(author=ctx.author, message=message)
        abnos = await get_site_content_json(
            "https://malcute.aeonmoon.page/api/lor/abno/"
        )

        list_of_name = []
        exists = False
        for abno in abnos:
            if abno["name"].lower() == search.lower():
                true_abno = abno
                exists = True
                break
            list_of_name.append(abno["name"].lower())

        if not exists:
            best_match = process.extractOne(
                search.lower(), list_of_name, scorer=fuzz.ratio
            )
            best_match = best_match[0]
            true_abno = [x for x in abnos if x["name"].lower() == best_match]
            true_abno = true_abno[0]
        id_of_abno = true_abno["id"]
        name = true_abno["name"]
        effect = true_abno["effects"]
        description = true_abno["description"]
        emotion_type = true_abno["emotion_type"]
        if emotion_type == "BD":
            emotion_type = "Breakdown"
        else:
            emotion_type = "Awakening"
        emotion_level = true_abno["emotion_level"]
        office = true_abno["office"]
        general_info_str = f"""
        > Emotion Type: {emotion_type}
        > Emotion Level: {emotion_level}
        > Floor: {office}
        """
        embed = discord.Embed()
        embed.color = 3447003
        embed.set_author(name=name)
        embed.description = general_info_str
        embed.add_field(name="Description", value=description)
        embed.add_field(name="Effect", value=effect)
        embed.set_footer(text=f"{LINK}/lor/abno/{id_of_abno}")
        ImgPath = true_abno["ImgPath"]
        if ImgPath[:8] == "lor_data" or ImgPath[:8] == "LoR_Data":
            ImgPath = ImgPath.replace(" ", "%20")
            embed.set_image(
                url=f"https://malcute.aeonmoon.page/django_static/{ImgPath}"
            )
        else:
            embed.set_image(url=ImgPath)

        return await message.edit(
            content="Here is the best match",
            embed=embed,
            view=delete_button,
        )

    @commands.hybrid_command()
    async def abno(self, ctx, *, search: str):
        """?abno <card name> Looks for abnormality cards from the gam"""
        if ctx.message.guild.id != 718294958573879347:
            await self.searchAbno(ctx, search)

        else:
            if ctx.message.channel.id in self.allowed_channel:
                await self.searchAbno(ctx, search)
            else:
                await ctx.send("This command is not allowed in this channel.")

    @commands.hybrid_command()
    async def effect(self, ctx, *, search: str):
        """?effect <passive name> Looks for best matched passive"""
        message = await ctx.send("Loading...")
        delete_button = DeleteEmbedView(author=ctx.author, message=message)
        effs = await get_site_content_json(
            "https://malcute.aeonmoon.page/api/lor/effects"
        )
        list_of_effects = []
        exists = False
        for obs in effs:
            if obs["Name"].lower() == search.lower():
                embed = discord.Embed()
                embed.set_author(name=obs["Name"])
                description = obs["Description"]
                embed.add_field(name="Cost", value=obs["Cost"])
                embed.add_field(name="Rarity", value=Rarity_dict[obs["Rarity"]])
                embed.add_field(name="Transferable", value=obs["Transferable"])
                embed.add_field(name="Rank", value=obs["Rank"])
                embed.add_field(name="Guest", value=obs["Guest"])
                embed.add_field(name="Description", value=description)
                embed.color = color_dict[Rarity_dict[obs["Rarity"]]]
                await message.edit(embed=embed, view=delete_button)
                exists = True
            else:
                list_of_effects.append(obs["Name"].lower())

        if not exists:
            best_match = process.extractOne(
                search.lower(), list_of_effects, scorer=fuzz.ratio
            )
            best_match = best_match[0]
            true_eff = [x for x in effs if x["Name"].lower() == best_match]
            true_eff = true_eff[0]
            embed = discord.Embed()
            embed.set_author(name=true_eff["Name"])
            description = true_eff["Description"]
            embed.add_field(name="Cost", value=true_eff["Cost"])
            embed.add_field(name="Rarity", value=Rarity_dict[true_eff["Rarity"]])
            embed.add_field(name="Transferable", value=true_eff["Transferable"])
            embed.add_field(name="Rank", value=true_eff["Rank"])
            embed.add_field(name="Guest", value=true_eff["Guest"])
            embed.add_field(name="Description", value=description, inline=False)
            embed.color = color_dict[Rarity_dict[true_eff["Rarity"]]]
            await message.edit(
                content="Name not found! Here is the best match",
                embed=embed,
                view=delete_button,
            )

    @commands.command()
    async def interview(self, ctx):
        """Sends a list of past Project Moon Interviews"""
        THIS_LINK = "https://malcute.aeonmoon.page/api/interview"
        data = await get_site_content_json(THIS_LINK)
        embed = discord.Embed()
        embed.set_author(name="Interviews")
        names = ""
        links_string = ""
        posted_dates = ""
        for datas in data:
            interview_name = datas["name"]
            number = datas["id"]
            link = f"[Link Here](https://aeonmoon.vercel.app/interview/{number})"
            names += interview_name
            names += "\n"
            links_string += link
            links_string += "\n"
            posted_dates += datas["date"]
            posted_dates += "\n"
        embed.add_field(name="Name", value=names, inline=True)
        embed.add_field(name="Link", value=links_string, inline=True)
        embed.add_field(name="Date", value=posted_dates, inline=True)
        embed.set_footer(text="Source: https://aeonmoon.vercel.app/interview")
        await ctx.send(embed=embed)

    @commands.hybrid_command()
    async def page(self, ctx, *, search: str):
        """?page <page name> Looks for best matched page"""
        message = await ctx.send("Loading...")
        delete_button = DeleteEmbedView(author=ctx.author, message=message)
        pages = await get_site_content_json(
            "https://malcute.aeonmoon.page/api/lor/page"
        )

        list_of_pages = []
        for obs in pages:
            list_of_pages.append(obs["Name"].lower())
        best_match = process.extractOne(
            search.lower(), list_of_pages, scorer=fuzz.ratio
        )
        best_match = best_match[0]
        true_page = [x for x in pages if x["Name"].lower() == best_match]
        true_page = true_page[0]
        embed = discord.Embed()
        embed.set_author(name=true_page["Name"])
        embed.description = f"""
            Guest: {true_page['office']}
            Rarity: {true_page['Rarity']}
            HP: {true_page['HP']} || Stagger: {true_page['Stagger']}
            Type: {true_page['RangeType']}
            Speed Dice: {true_page['SpeedMin']}-{true_page["Speed"]}
                        """
        HP_string = f"""
        Slash : {true_page['SlashResist']}
        Pierce : {true_page['PierceResist']}
        Blunt : {true_page['BluntResist']}
        """
        Stagger_string = f"""
        Slash : {true_page['SlashStaggerResist']}
        Pierce : {true_page['PierceStaggerResist']}
        Blunt : {true_page['BluntStaggerResist']}
        """
        embed.color = color_dict[true_page["Rarity"]]
        embed.add_field(name="HP Resist", value=HP_string, inline=True)
        embed.add_field(name="Stagger Resist", value=Stagger_string, inline=True)
        passive_string = ""
        for passive in true_page["InitialEffects"]:
            passive_string += passive["Name"]
            passive_string += "\n"
        if len(true_page["InitialEffects"]) == 0:
            passive_string = "None"
        embed.add_field(name="Passives", value=passive_string, inline=False)
        await message.edit(
            content="Here is the best match",
            embed=embed,
            view=delete_button,
        )


async def setup(bot):
    await bot.add_cog(searchCard(bot))
