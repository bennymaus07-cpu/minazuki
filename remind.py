import discord, asyncio, re
from discord.ext import commands
from discord import app_commands

class Reminders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_reminders = {} # Speicher für die Session

    @app_commands.command(name="remind", description="🕧 Setzt eine Erinnerung")
    async def remind(self, itxn: discord.Interaction, zeit: str, grund: str):
        match = re.match(r"(\d+)([smhd])", zeit.lower())
        if not match:
            return await itxn.response.send_message("❌ Format: `10m`, `2h`, `1d`!", ephemeral=True)

        sek = {"s": 1, "m": 60, "h": 3600, "d": 86400}[match.group(2)] * int(match.group(1))

        rid = len(self.active_reminders) + 1
        self.active_reminders[rid] = {"user": itxn.user.name, "task": grund, "time": zeit}

        await itxn.response.send_message(f"✅ ID #{rid} registriert. Erinnere in **{zeit}**.")

        await asyncio.sleep(sek)
        if rid in self.active_reminders:
            await itxn.channel.send(f"🔔 {itxn.user.mention}: **{grund}**")
            del self.active_reminders[rid]

    @app_commands.command(name="remind_list", description="📋 Zeigt aktive Erinnerungen")
    async def list_remind(self, itxn: discord.Interaction):
        if not self.active_reminders:
            return await itxn.response.send_message("Aktuell keine Timer aktiv.", ephemeral=True)

        text = "\n".join([f"**#{k}** | {v['time']} | {v['task']}" for k, v in self.active_reminders.items()])
        emb = discord.Embed(title="⏰ Aktive Erinnerungen", description=text, color=0xFFFFFF)
        await itxn.response.send_message(embed=emb)

async def setup(bot): await bot.add_cog(Reminders(bot))