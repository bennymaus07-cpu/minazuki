import discord
from discord.ext import commands
from discord import app_commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="reload", description="📁 Aktualisiert eine Cog (Owner only)")
    async def reload(self, itxn: discord.Interaction, cog_name: str):
        if not await self.bot.is_owner(itxn.user):
            return await itxn.response.send_message("❌ Kein Zugriff.", ephemeral=True)

        try:
            await self.bot.reload_extension(f"cogs.{cog_name}")
            await itxn.response.send_message(f"✅ `cogs.{cog_name}` neu geladen!")
        except Exception as e:
            await itxn.response.send_message(f"❌ Fehler: {e}", ephemeral=True)

async def setup(bot): await bot.add_cog(Admin(bot))