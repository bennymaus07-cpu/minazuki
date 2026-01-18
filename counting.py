import discord, json, os
from discord.ext import commands
from discord import app_commands

class CountingPro(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file = "counting_data.json"
        self.db = self.load_db()

    def load_db(self):
        if os.path.exists(self.file):
            with open(self.file, "r") as f: return json.load(f)
        return {}

    def save_db(self):
        with open(self.file, "w") as f: json.dump(self.db, f, indent=4)

    @app_commands.command(name="counting_setup", description="🔢 Richtet den Channel ein")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup(self, itxn: discord.Interaction, channel: discord.TextChannel):
        self.db[str(itxn.guild_id)] = {
            "channel": channel.id, "count": 0, "last_user": None, "highscore": 0
        }
        self.save_db()
        await itxn.response.send_message(f"✅ Setup in {channel.mention} abgeschlossen!")

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot or not msg.guild: return
        gid = str(msg.guild.id)
        if gid not in self.db or msg.channel.id != self.db[gid]["channel"]: return

        try:
            val = int(msg.content)
            data = self.db[gid]
            next_val = data["count"] + 1

            if val == next_val and msg.author.id != data["last_user"]:
                data["count"] = val
                data["last_user"] = msg.author.id
                if val > data["highscore"]: data["highscore"] = val
                self.save_db()
                await msg.add_reaction("☑️")
            else:
                reason = "Falsche Zahl" if val != next_val else "Nicht zweimal hintereinander!"
                data["count"] = 0
                data["last_user"] = None
                self.save_db()
                await msg.add_reaction("❌")
                await msg.channel.send(f"💥 {msg.author.mention} hat versagt! ({reason})\n🏆 Highscore: **{data['highscore']}**")
        except ValueError: pass

async def setup(bot): await bot.add_cog(CountingPro(bot))