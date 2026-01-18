import discord
from discord.ext import commands
from discord import app_commands

DEV_IDS = [1461462642626396375] # Deine ID

class SayCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="say", description="📢 Sendet eine Nachricht als Bot")
    @app_commands.describe(nachricht="Der Text, den der Bot sagen soll", kanal="Optionaler Kanal für die Nachricht")
    async def say(self, itxn: discord.Interaction, nachricht: str, kanal: discord.TextChannel = None):
        # Berechtigung: Admin oder Developer
        if not (itxn.user.guild_permissions.administrator or itxn.user.id in DEV_IDS):
            return await itxn.response.send_message(" Zugriff verweigert.", ephemeral=True)

        target = kanal or itxn.channel

        try:
            await target.send(nachricht)
            await itxn.response.send_message(f"✅ Nachricht in {target.mention} gesendet.", ephemeral=True)
        except discord.Forbidden:
            await itxn.response.send_message("❌ Fehler: Keine Rechte in diesem Kanal.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(SayCog(bot))