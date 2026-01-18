import discord
from discord.ext import commands
from discord import app_commands

class CommandLab(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.test_guild_id = 1459233271471800424  # DEINE TEST-SERVER ID

    @app_commands.command(name="lab_sync", description="🧪 Synchronisiert Befehle NUR auf den Test-Server")
    async def lab_sync(self, itxn: discord.Interaction):
        if not await self.bot.is_owner(itxn.user): return

        # Kopiert alle globalen Commands in die Test-Guild
        test_guild = discord.Object(id=self.test_guild_id)
        self.bot.tree.copy_global_to(guild=test_guild)
        synced = await self.bot.tree.sync(guild=test_guild)

        await itxn.response.send_message(f"🧪 **Lab-Sync erfolgreich!** {len(synced)} Befehle im Test-Modus verfügbar.", ephemeral=True)

    @app_commands.command(name="lab_publish", description="🧑‍🏫 Veröffentlicht alle Befehle GLOBAL")
    async def lab_publish(self, itxn: discord.Interaction):
        if not await self.bot.is_owner(itxn.user): return

        await itxn.response.defer(ephemeral=True)
        synced = await self.bot.tree.sync() # Ohne Guild = Global
        await itxn.followup.send(f"🌍 **Globaler Rollout!** {len(synced)} Befehle sind nun für alle Server live.")

    @app_commands.command(name="lab_clear", description="🧽 Löscht alle Commands vom Test-Server")
    async def lab_clear(self, itxn: discord.Interaction):
        if not await self.bot.is_owner(itxn.user): return

        test_guild = discord.Object(id=self.test_guild_id)
        self.bot.tree.clear_commands(guild=test_guild)
        await self.bot.tree.sync(guild=test_guild)
        await itxn.response.send_message("🧹 Test-Server gesäubert.", ephemeral=True)

async def setup(bot): await bot.add_cog(CommandLab(bot))