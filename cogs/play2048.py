from discord.ext import commands
from datetime import datetime
import asyncio
from utils.Utils2048 import (
    start,
    right,
    left,
    up,
    down,
    gameOver,
    win,
    formTable,
    spawnNew,
)


class play2048(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.on_going = False
        self.sent_msg = None
        self.player = None
        self.grid = start()

    async def quit_game(self):
        self.on_going = False
        self.player = None

    @commands.group()
    async def tzfe(self, ctx):
        """Play 2048, a legendary game!"""
        if ctx.invoked_subcommand is None:
            if self.on_going:
                if (datetime.utcnow() - self.on_going).total_seconds() > 120:
                    await self.quit_game()
                    self.on_going = False
            if not self.on_going:
                self.on_going = datetime.utcnow()
                self.player = ctx.author
                self.grid = start()
                self.sent_msg = await ctx.send(content=f"```{formTable(self.grid)}```")
                self.bot.loop.create_task(self.timer())
                await self.sent_msg.add_reaction("⬅️")
                await self.sent_msg.add_reaction("⬆️")
                await self.sent_msg.add_reaction("➡️")
                await self.sent_msg.add_reaction("⬇️")

            else:
                await ctx.send("There is currently a game in session, please wait!")

    @tzfe.command()
    async def quit(self, ctx):
        """Quit tzfe game"""
        if ctx.author == self.player and self.on_going:
            self.on_going = False
            await ctx.send("Ending game")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, event):
        if (
            self.on_going
            and (event.emoji.name in ("⬅️", "⬆️", "➡️", "⬇️"))
            and event.message_id == self.sent_msg.id
            and event.user_id != self.bot.user.id
            and self.player.id == event.user_id
        ):
            self.on_going = datetime.utcnow()
            if event.emoji.name == "⬅️":
                temp = left(self.grid)
                del self.grid
                self.grid = temp
                # This is to tell what msg to edit
                self.sent_msg = await self.bot.get_channel(
                    event.channel_id
                ).fetch_message(event.message_id)
                if win(self.grid):
                    await self.sent_msg.channel.send("You won congrats!")
                    await self.quit_game()
                elif gameOver(self.grid):
                    await self.sent_msg.channel.send("You lost, GG!")
                    await self.quit_game()
                spawnNew(self.grid)
                await self.sent_msg.edit(content=f"```{formTable(self.grid)}```")
                await self.sent_msg.remove_reaction(event.emoji, self.player)
            elif event.emoji.name == "⬆️":
                temp = up(self.grid)
                del self.grid
                self.grid = temp
                self.sent_msg = await self.bot.get_channel(
                    event.channel_id
                ).fetch_message(event.message_id)
                if win(self.grid):
                    await self.sent_msg.channel.send("You won congrats!")
                    await self.quit_game()
                elif gameOver(self.grid):
                    await self.sent_msg.channel.send("You lost, GG!")
                    await self.quit_game()
                spawnNew(self.grid)
                await self.sent_msg.edit(content=f"```{formTable(self.grid)}```")
                await self.sent_msg.remove_reaction(event.emoji, self.player)
            elif event.emoji.name == "➡️":
                temp = right(self.grid)
                del self.grid
                self.grid = temp
                self.sent_msg = await self.bot.get_channel(
                    event.channel_id
                ).fetch_message(event.message_id)
                if win(self.grid):
                    await self.sent_msg.channel.send("You won congrats!")
                    await self.quit_game()
                elif gameOver(self.grid):
                    await self.sent_msg.channel.send("You lost, GG!")
                    await self.quit_game()
                spawnNew(self.grid)
                await self.sent_msg.edit(content=f"```{formTable(self.grid)}```")
                await self.sent_msg.remove_reaction(event.emoji, self.player)
            elif event.emoji.name == "⬇️":
                temp = down(self.grid)
                del self.grid
                self.grid = temp
                self.sent_msg = await self.bot.get_channel(
                    event.channel_id
                ).fetch_message(event.message_id)
                if win(self.grid):
                    await self.sent_msg.channel.send("You won congrats!")
                    await self.quit_game()
                elif gameOver(self.grid):
                    await self.sent_msg.channel.send("You lost, GG!")
                    await self.quit_game()
                spawnNew(self.grid)
                await self.sent_msg.edit(content=f"```{formTable(self.grid)}```")
                await self.sent_msg.remove_reaction(event.emoji, self.player)

    async def timer(self):
        while self.on_going:
            time_left = (datetime.utcnow() - self.on_going).total_seconds()
            if time_left > 120:
                await self.sent_msg.channel.send(
                    f"@{str(self.player)} gone for 2 mins. Clearing."
                )
                await self.quit_game()
            await asyncio.sleep(2)


async def setup(bot):
    await bot.add_cog(play2048(bot))
