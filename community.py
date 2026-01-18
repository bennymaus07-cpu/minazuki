import discord, json, os, datetime
from discord.ext import commands
from discord import app_commands
from discord.ui import Select, View


class DailyView(View):
    def __init__(self, cog, user_id):
        super().__init__(timeout=60)
        self.cog = cog
        self.user_id = str(user_id)

    @discord.ui.select(
        placeholder="Wähle eine Option...",
        options=[
            discord.SelectOption(label="Daily Reward", description="Sammle 100 Credits", emoji="🎁"),
            discord.SelectOption(label="Konto-Details", description="Sieh dein Guthaben ein", emoji="📊")
        ]
    )
    async def select_callback(self, itxn: discord.Interaction, select: Select):
        if str(itxn.user.id) != self.user_id:
            return await itxn.response.send_message("❌ Nicht dein Menü!", ephemeral=True)

        data = self.cog.load_data()
        user_data = data["profiles"].get(self.user_id, {"credits": 0, "last_daily": None})

        if select.values[0] == "Daily Reward":
            now = datetime.datetime.now()
            last = user_data.get("last_daily")
            if last and (now - datetime.datetime.fromisoformat(last)).total_seconds() < 86400:
                return await itxn.response.send_message("⏳ Morgen wieder!", ephemeral=True)

            user_data["credits"] += 1000
            user_data["last_daily"] = now.isoformat()
            data["profiles"][self.user_id] = user_data
            self.cog.save_data(data)
            await itxn.response.send_message("✨ 1000 Credits erhalten!", ephemeral=True)
        else:
            await itxn.response.send_message(f"💰 Kontostand: {user_data['credits']} Credits", ephemeral=True)


class Community(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = "users.json"

    def load_data(self):
        if os.path.exists(self.db):
            with open(self.db, "r") as f: return json.load(f)
        return {"profiles": {}}

    def save_data(self, data):
        with open(self.db, "w") as f: json.dump(data, f, indent=4)

    @app_commands.command(name="daily", description="💴 Täglicher Bonus")
    async def daily(self, itxn: discord.Interaction):
        embed = discord.Embed(title="Rewards System", color=0xFFFFFF)
        embed.add_field(name="Credits", value="**Solltest du KEINE 1000 Credits bekomnmen, melde diesen Fehler bitte bei Hedi ODER bei minazuki.**", inline=False)
        embed.add_field(name="Credits", value="1000 Credits", inline=False)
        embed.add_field(name="Cooldown", value="24 Stunden", inline=False)
        embed.set_thumbnail(url=itxn.user.display_avatar.url)
        await itxn.response.send_message(embed=embed, view=DailyView(self, itxn.user.id))

async def setup(bot):
    await bot.add_cog(Community(bot))