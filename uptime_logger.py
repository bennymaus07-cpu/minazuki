import discord, time
from discord.ext import commands
from discord import app_commands
from datetime import datetime

class Uptime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()

    @app_commands.command(name="uptime", description="💾 Zeigt wie lange der Bot online ist")
    async def uptime(self, itxn: discord.Interaction):
        delta = int(time.time() - self.start_time)
        hours, remainder = divmod(delta, 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        msg = f"⏳ Online seit: **{days}d {hours}h {minutes}m {seconds}s**"
        await itxn.response.send_message(msg)

async def setup(bot): await bot.add_cog(Uptime(bot))