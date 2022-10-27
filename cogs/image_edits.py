from discord.errors import DiscordException
from discord.ext import commands
import discord
import aiohttp
import os
from PIL import Image, ImageOps

FILE_NAME_2 = "./data/Patbanlist.txt"


class ImageEdits(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.banlist = set()
        with open(FILE_NAME_2, "r") as f:
            for i in f.read().split("\n"):
                if len(i) > 0:
                    self.banlist.add(int(i))

    @commands.command()
    async def disable_pat(self, ctx, mentioned_user: discord.Member = None):
        """Allows certain users to disable patting in Community server"""
        arx = int(mentioned_user.id)
        if (
            ctx.message.author.id == self.bot.config["discord"]["owner"]
            or ctx.message.author.id in self.bot.config["discord"]["Ruina_Mods"]
        ):
            self.banlist.add(arx)
            with open(FILE_NAME_2, "a") as f:
                f.write(f"\n{arx}")
            await ctx.send(f"Banned {mentioned_user} from patting")
        else:
            await ctx.send("You are not allowed to use this command")

    @commands.command()
    async def enable_pat(self, ctx, mentioned_user: discord.Member = None):
        """Allows certain users to disable patting in Community server"""
        arx = int(mentioned_user.id)
        if (
            ctx.message.author.id == self.bot.config["discord"]["owner"]
            or ctx.message.author.id in self.bot.config["discord"]["Ruina_Mods"]
        ):
            self.banlist.remove(arx)
            with open(FILE_NAME_2, "w") as f:
                f.write("\n".join(list(map(str, self.banlist))))
            await ctx.send(f"Unbanned {mentioned_user} from patting")
        else:
            await ctx.send("You are not allowed to use this command")

    @commands.command()
    async def pat(self, ctx, mentioned_user: discord.Member = None):
        """Pat people! ?pat @user"""
        if ctx.message.guild.id == 718294958573879347 and (
            ctx.message.author.id in self.banlist
            and ctx.message.channel.id != 718306312131313694
        ):
            await ctx.send(
                "You are banned from using this command in LoR community discord server."
            )
        else:
            try:
                if not mentioned_user:
                    return await ctx.send("You have to tag a user to pat them!")
                else:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(
                            str(mentioned_user.avatar_url_as(format="png"))
                        ) as resp:
                            if resp.status == 200:
                                avatar_content = await resp.read()
                    with open("tmp/tmp2.png", "wb") as f:
                        f.write(avatar_content)
                    avatar = Image.open("tmp/tmp2.png")
                    pat1 = Image.open("./data/Headpat/Headpat 01.png")
                    pat2 = Image.open("./data/Headpat/Headpat 02.png")
                    pat3 = Image.open("./data/Headpat/Headpat 03.png")
                    pat4 = Image.open("./data/Headpat/Headpat 04.png")
                    pat5 = Image.open("./data/Headpat/Headpat 05.png")
                    mask = Image.open("./data/mask.png").convert("L")
                    output = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
                    output.putalpha(mask)
                    frame = []
                    newImg = Image.new("RGBA", (200, 200), (54, 57, 62, 0))
                    newImg.paste(output, (20, 40), output)
                    newImg.paste(pat1, (0, 0), pat1)
                    frame.append(newImg)
                    newImg = Image.new("RGBA", (200, 200), (54, 57, 62, 0))
                    newImg.paste(output, (20, 40), output)
                    newImg.paste(pat2, (0, 0), pat2)
                    frame.append(newImg)
                    newImg = Image.new("RGBA", (200, 200), (54, 57, 62, 0))
                    newImg.paste(
                        output.resize((133, 118)), (20, 50), output.resize((133, 118))
                    )
                    newImg.paste(pat3, (0, 0), pat3)
                    frame.append(newImg)
                    newImg = Image.new("RGBA", (200, 200), (54, 57, 62, 0))
                    newImg.paste(
                        output.resize((138, 108)), (20, 60), output.resize((138, 108))
                    )
                    newImg.paste(pat4, (0, 0), pat4)

                    frame.append(newImg)
                    newImg = Image.new("RGBA", (200, 200), (54, 57, 62, 0))
                    newImg.paste(
                        output.resize((133, 123)), (20, 55), output.resize((133, 123))
                    )
                    newImg.paste(pat5, (0, 0), pat5)
                    frame.append(newImg)

                    frame[0].save(
                        "tmp/pat.gif",
                        format="GIF",
                        save_all=True,
                        append_images=frame[1:],
                        duration=60,
                        loop=0,
                        optimize=False,
                        disposal=2,
                        transparency=0,
                        version="GIF89a",
                    )
                    with open("tmp/pat.gif", "rb") as f:
                        await ctx.send(content=None, file=discord.File(f))
                    # os.remove("tmp/tmp2.png")
                    # os.remove("tmp/pat.gif")
            except discord.ext.commands.errors.BadArgument:
                await ctx.send("That person doesn't exist!")

    @commands.command()
    async def pat2(self, ctx, img_link: str = None, x=0.5, y=0.5):
        """Pat people! ?pat2 <image-link>"""
        try:
            if not img_link:
                return await ctx.send("You have to give image link to pat them!")
            else:
                if img_link[0] == "<":
                    img_link = img_link[1 : len(img_link) - 1]
                async with aiohttp.ClientSession() as session:
                    async with session.get(img_link) as resp:
                        if resp.status == 200:
                            image = await resp.read()
                with open("tmp/tmp2.png", "wb") as f:
                    f.write(image)
                avatar = Image.open("tmp/tmp2.png")
                pat1 = Image.open("./data/Headpat/Headpat 01.png")
                pat2 = Image.open("./data/Headpat/Headpat 02.png")
                pat3 = Image.open("./data/Headpat/Headpat 03.png")
                pat4 = Image.open("./data/Headpat/Headpat 04.png")
                pat5 = Image.open("./data/Headpat/Headpat 05.png")
                mask = Image.open("./data/mask.png").convert("L")
                output = ImageOps.fit(avatar, mask.size, centering=(x, y))
                output.putalpha(mask)
                frame = []
                newImg = Image.new("RGBA", (200, 200), (54, 57, 62, 0))
                newImg.paste(output, (20, 40), output)
                newImg.paste(pat1, (0, 0), pat1)
                frame.append(newImg)
                newImg = Image.new("RGBA", (200, 200), (54, 57, 62, 0))
                newImg.paste(output, (20, 40), output)
                newImg.paste(pat2, (0, 0), pat2)
                frame.append(newImg)
                newImg = Image.new("RGBA", (200, 200), (54, 57, 62, 0))
                newImg.paste(
                    output.resize((133, 118)), (20, 50), output.resize((133, 118))
                )
                newImg.paste(pat3, (0, 0), pat3)
                frame.append(newImg)
                newImg = Image.new("RGBA", (200, 200), (54, 57, 62, 0))
                newImg.paste(
                    output.resize((138, 108)), (20, 60), output.resize((138, 108))
                )
                newImg.paste(pat4, (0, 0), pat4)

                frame.append(newImg)
                newImg = Image.new("RGBA", (200, 200), (54, 57, 62, 0))
                newImg.paste(
                    output.resize((133, 123)), (20, 55), output.resize((133, 123))
                )
                newImg.paste(pat5, (0, 0), pat5)
                frame.append(newImg)

                frame[0].save(
                    "tmp/pat.gif",
                    format="GIF",
                    save_all=True,
                    append_images=frame[1:],
                    duration=60,
                    loop=0,
                    disposal=2,
                    optimize=False,
                    transparency=0,
                    version="GIF89a",
                )
                with open("tmp/pat.gif", "rb") as f:
                    await ctx.send(content=None, file=discord.File(f))
                # os.remove("tmp/tmp2.png")
                # os.remove("tmp/pat.gif")
        except discord.ext.commands.errors.BadArgument:
            await ctx.send("That person doesn't exist!")


async def setup(bot):
    await bot.add_cog(ImageEdits(bot))
