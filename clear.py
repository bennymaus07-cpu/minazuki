import discord
from discord.ext import commands
from discord import app_commands

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="clear", description="🪄 Löscht Nachrichten")
    async def clear(self, itxn: discord.Interaction, anzahl: int):
        is_owner = await self.bot.is_owner(itxn.user)
        has_perms = itxn.user.guild_permissions.manage_messages

        if not (is_owner or has_perms):
            return await itxn.response.send_message("❌ Keine Rechte!", ephemeral=True)

        await itxn.response.defer(ephemeral=True)
        deleted = await itxn.channel.purge(limit=anzahl)
        await itxn.followup.send(f"✅ {len(deleted)} Nachrichten gelöscht.")

async def setup(bot): await bot.add_cog(Utility(bot))