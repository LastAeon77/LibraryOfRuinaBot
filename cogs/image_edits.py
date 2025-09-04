from discord.errors import DiscordException
from discord.ext import commands
import discord
import aiohttp
import os
import io
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
        if ctx.guild and ctx.guild.id == 718294958573879347 and ctx.author.id in self.banlist:
            return await ctx.send(
                "You are banned from using this command in LoR community discord server."
            )

        if not mentioned_user:
            return await ctx.send("You have to tag a user to pat them!")

        try:
            # Fetch user's avatar
            async with aiohttp.ClientSession() as session:
                avatar_url = mentioned_user.display_avatar.with_format("png").url
                async with session.get(avatar_url) as resp:
                    if resp.status != 200:
                        return await ctx.send("Failed to fetch avatar.")
                    avatar_bytes = await resp.read()

            avatar = Image.open(io.BytesIO(avatar_bytes)).convert("RGBA")

            # Load pat overlays and mask
            pats = [Image.open(f"./data/Headpat/Headpat 0{i}.png").convert("RGBA") for i in range(1,6)]
            mask = Image.open("./data/mask.png").convert("L")

            # Prepare avatar with mask
            output = ImageOps.fit(avatar, mask.size, centering=(0.5,0.5))
            output.putalpha(mask)

            # Bounce positions for avatar
            y_offsets = [40, 35, 30, 35, 40]  # up and down
            avatar_sizes = [output.size, output.size, (133,118), (138,108), (133,123)]

            frames = []

            for i in range(5):
                frame_img = Image.new("RGBA", (200,200), (54,57,62,0))
                resized_avatar = output if avatar_sizes[i] == output.size else output.resize(avatar_sizes[i])
                frame_img.paste(resized_avatar, (20, y_offsets[i]), resized_avatar)
                frame_img.paste(pats[i], (0,0), pats[i])
                frames.append(frame_img)

            # Save GIF in memory with disposal=2 to prevent ghosting
            with io.BytesIO() as gif_buffer:
                frames[0].save(
                    gif_buffer,
                    format="GIF",
                    save_all=True,
                    append_images=frames[1:],
                    duration=60,
                    loop=0,
                    disposal=2
                )
                gif_buffer.seek(0)
                await ctx.send(file=discord.File(gif_buffer, "pat.gif"))

        except discord.ext.commands.BadArgument:
            await ctx.send("That person doesn't exist!")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")



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
