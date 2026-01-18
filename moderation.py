import discord
from discord.ext import commands
from discord import app_commands, ui
from datetime import timedelta

DEV_IDS = [1461462642626396375] # DEINE ID

class ModModal(ui.Modal):
    reason = ui.TextInput(label="Begründung", style=discord.TextStyle.paragraph, min_length=5)

    def __init__(self, target, action, duration=None, cog=None):
        super().__init__(title=f"Core | Execution: {action}")
        self.target, self.action, self.duration, self.cog = target, action, duration, cog

    async def on_submit(self, itxn: discord.Interaction):
        try:
            res = self.reason.value
            if self.action == "Ban": await self.target.ban(reason=res)
            elif self.action == "Kick": await self.target.kick(reason=res)
            elif self.action == "Warn": self.cog.warns.setdefault(self.target.id, []).append(res)
            elif self.action == "Timeout": 
                await self.target.timeout(discord.utils.utcnow() + timedelta(minutes=self.duration), reason=res)

            emb = discord.Embed(title=" System Action Executed", color=0x2b2d31)
            emb.description = f"**Target:** {self.target.mention}\n**Action:** {self.action}\n**Reason:** {res}"
            if self.action == "Warn": emb.description += f"\n**Total Warns:** {len(self.cog.warns[self.target.id])}"

            await itxn.response.send_message(embed=emb)
        except discord.Forbidden:
            await itxn.response.send_message("❌ **Fehler:** Fehlende Berechtigung!", ephemeral=True)

class ModView(ui.View):
    def __init__(self, target, cog):
        super().__init__(timeout=60)
        self.target, self.cog = target, cog

    @ui.select(placeholder="🛑 Wähle eine Sanktion aus...", options=[
        discord.SelectOption(label="Warn", description="Verwarnung aussprechen", emoji="⚠️"),
        discord.SelectOption(label="Timeout (1h)", description="Mute für 1 Std", value="tm_60", emoji="⏳"),
        discord.SelectOption(label="Timeout (MAX)", description="Mute für 28 Tage", value="tm_40320", emoji="♾️"),
        discord.SelectOption(label="Kick", description="Vom Server entfernen", emoji="👢"),
        discord.SelectOption(label="Ban", description="Dauerhafter Bann", emoji="🚫")
    ])
    async def select_callback(self, itxn: discord.Interaction, select: ui.Select):
        v = select.values[0]
        if v.startswith("tm_"): await itxn.response.send_modal(ModModal(self.target, "Timeout", int(v[3:])))
        else: await itxn.response.send_modal(ModModal(self.target, v, cog=self.cog))

class Moderation(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot
        self.warns = {} # Hier werden Warns gespeichert (für DB später erweitern)

    @app_commands.command(name="execute", description="🛡️Admin Execution Tool")
    async def execute(self, itxn: discord.Interaction, user: discord.Member):
        if not (itxn.user.guild_permissions.moderate_members or itxn.user.id in DEV_IDS):
            return await itxn.response.send_message("⛔ Zugriff verweigert!", ephemeral=True)
        await itxn.response.send_message(embed=discord.Embed(title=" Moderation Panel", color=0xFFFFFF), view=ModView(user, self), ephemeral=True)

async def setup(bot): await bot.add_cog(Moderation(bot))