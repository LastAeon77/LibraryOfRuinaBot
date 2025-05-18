from discord.ext import commands
from discord import app_commands
import discord
from datetime import datetime, timedelta
from CustomClasses.API import malkTalk
import json
import random

class Summary(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def prompt_load(self):
        with open("./data/MalkTalk.json",'r') as f:
            data = json.loads(f.read())
            prompts = data['prompt']
            prompt = random.choice(list(prompts.values()))
            default_string = ' '.join(prompt)
            abnos = data['abno']
            abnos = random.sample(abnos,4)
            abno_string = []
            for a in abnos:
                abno_string.append(f"{a['name']} ({a['quirk']})")
            abno_string = ', '.join(abno_string)
            default_string = default_string.replace("<ABNOREPLACE>",abno_string)
            return default_string

    @app_commands.command(name="summarize", description="Malcute shall do her best to summarize.")
    @app_commands.describe(num="Number of messages to summarize (between 30 and 100)")
    async def summarize(self, interaction: discord.Interaction, num: int):
        SHUTDOWN = False  # Or reference your global shutdown variable appropriately
        if SHUTDOWN:
            await interaction.response.send_message(
                "Everyone is being a misbehaving naughty little clerk so this request is no longer authorized.", 
                ephemeral=True
            )
            return

        if num > 100:
            await interaction.response.send_message(
                "Oh Darling little clerk, don't try to push so much on my plate and try reading on your own, wouldn't you?", 
                ephemeral=True
            )
            return

        member = interaction.user
        one_month_ago = datetime.now().replace(tzinfo=None) - timedelta(days=30)
        if member.joined_at and member.joined_at.replace(tzinfo=None) > one_month_ago:
            await interaction.response.send_message(
                "You need to have stayed in this server for longer than 1 month for this command to work, little agent.",
                ephemeral=True
            )
            return

        await interaction.response.defer(ephemeral=True)
        messages = []
        channel = interaction.channel
        useless_messages = 0

        async for message in channel.history(limit=num):
            if message.author.id != 688776393450192953 and not message.content.startswith("/summarize"):
                messages.append(f"'{message.author.display_name}': '{message.content}'")
            else:
                useless_messages += 1

        formatted_messages = "\n".join(messages[::-1])
        if len(formatted_messages) > 60000:
            await interaction.followup.send(
                "Oh little agent, that's a bit too many messages... try lowering the number.", 
                ephemeral=True
            )
            return

        result = await malkTalk(self.bot.config["AI"]["qwq-key"], await self.prompt_load(), formatted_messages)
        true_result = result.get("choices", [{}])[0].get("message", {}).get("content", "*Malcute is sleeping* zzz")

        await interaction.followup.send(true_result, ephemeral=True)

# Then add this to your bot during setup:
async def setup(bot):
    await bot.add_cog(Summary(bot))