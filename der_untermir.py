import discord
from discord.ext import commands
from discord import app_commands

class UnterMir(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="der_unter_mir", description="⬇️ Starte eine Runde 'Der Unter mir'")
    async def dum(self, itxn: discord.Interaction, spruch: str):
        embed = discord.Embed(
            title="👇 Der Unter mir...",
            description=f"**{itxn.user.display_name} sagt:**\n... {spruch}",
            color=discord.Color.blue()
        )
        embed.set_footer(text="Schreib einfach in den Chat, um zu antworten!")
        await itxn.response.send_message(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: return
        # Prüft ob die Nachricht auf ein "Der Unter mir" folgt (optionaler Filter)
        if "unter mir" in message.content.lower():
            await message.add_reaction("🤣")

async def setup(bot):
    await bot.add_cog(UnterMir(bot))