import discord, json, os, random
from discord.ext import commands
from discord import app_commands

DEV_IDS = [1461462642626396375] # DEINE ID

class StatusCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file = "status_config.json"

    @commands.Cog.listener()
    async def on_ready(self):
        if os.path.exists(self.file):
            with open(self.file, "r") as f:
                d = json.load(f)
            # Presence beim Start wiederherstellen
            await self.update_presence(d['type'], d['text'], d['twitch'], d['status'])

    async def update_presence(self, typ, text, twitch, status):
        st = getattr(discord.Status, status)
        if typ == "streaming":
            act = discord.Streaming(name=text, url=f"https://twitch.tv/{twitch}")
        else:
            act = discord.Activity(type=getattr(discord.ActivityType, typ), name=text)
        await self.bot.change_presence(status=st, activity=act)

    @app_commands.command(name="status", description="🎮 Setzt den Bot Status")
    @app_commands.choices(typ=[
        app_commands.Choice(name="Streaming", value="streaming"),
        app_commands.Choice(name="Spielt", value="playing"),
        app_commands.Choice(name="Schaut zu", value="watching")
    ])
    async def set_status(self, itxn: discord.Interaction, typ: str, text: str, twitch_kanal: str = "twitch"):
        if itxn.user.id not in DEV_IDS and not itxn.user.guild_permissions.administrator:
            return await itxn.response.send_message("Kein Zugriff.", ephemeral=True)

        await self.update_presence(typ, text, twitch_kanal, "online")

        with open(self.file, "w") as f:
            json.dump({"type": typ, "text": text, "twitch": twitch_kanal, "status": "online"}, f)

        await itxn.response.send_message(f"✅ Status gesetzt: {typ} {text}", ephemeral=True)

async def setup(bot): await bot.add_cog(StatusCog(bot))