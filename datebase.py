import discord
from discord.ext import commands
from discord import app_commands
import json

class DatabaseManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="db_clean", description="🧹 Entfernt Daten von inaktiven Servern")
    async def db_clean(self, itxn: discord.Interaction):
        if not await self.bot.is_owner(itxn.user): return

        # Beispiel für das Säubern der Counting-DB
        with open("counting_data.json", "r+") as f:
            data = json.load(f)
            active_ids = [str(g.id) for g in self.bot.guilds]
            new_data = {k: v for k, v in data.items() if k in active_ids}

            removed = len(data) - len(new_data)
            f.seek(0)
            json.dump(new_data, f, indent=4)
            f.truncate()

        await itxn.response.send_message(f"✅ Datenbank bereinigt! `{removed}` tote Einträge gelöscht.", ephemeral=True)

async def setup(bot): await bot.add_cog(DatabaseManager(bot))