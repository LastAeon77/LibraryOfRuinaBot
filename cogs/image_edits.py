from discord.ext import commands
import discord
import aiohttp
import os
from PIL import Image, ImageOps


class ImageEdits(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pat(self, ctx, mentioned_user: discord.Member = None):
        """Pat people! ?pat @user"""
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
                #   36393E is the color of discord background. Gif can't have
                # transparent background.
                newImg = Image.new("RGB", (200, 200))
                newImg.paste(output, (20, 40), output)
                newImg.paste(pat1, (0, 0), pat1)
                frame.append(newImg)
                newImg = Image.new("RGB", (200, 200))
                newImg.paste(output, (20, 40), output)
                newImg.paste(pat2, (0, 0), pat2)
                frame.append(newImg)
                newImg = Image.new("RGB", (200, 200))
                newImg.paste(
                    output.resize((133, 118)), (20, 50), output.resize((133, 118))
                )
                newImg.paste(pat3, (0, 0), pat3)
                frame.append(newImg)
                newImg = Image.new("RGB", (200, 200))
                newImg.paste(
                    output.resize((138, 108)), (20, 60), output.resize((138, 108))
                )
                newImg.paste(pat4, (0, 0), pat4)
                frame.append(newImg)
                newImg = Image.new("RGB", (200, 200))
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
                    duration=50,
                    loop=0,
                )
                with open("tmp/pat.gif", "rb") as f:
                    await ctx.send(content=None, file=discord.File(f))
                os.remove("tmp/tmp2.png")
                os.remove("tmp/pat.gif")
        except discord.ext.commands.errors.BadArgument:
            await ctx.send("That person doesn't exist!")


def setup(bot):
    bot.add_cog(ImageEdits(bot))
