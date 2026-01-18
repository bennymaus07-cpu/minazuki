import discord
from discord.ext import commands
from discord import app_commands, ui

DEV_IDS = [1461462642626396375] # Deine ID

class TextModal(ui.Modal):
    def __init__(self, target, current_embed):
        super().__init__(title=f"Core | Edit {target}")
        self.target, self.current_embed = target, current_embed
        self.input = ui.TextInput(label="Inhalt", style=discord.TextStyle.paragraph if target == "Body" else discord.TextStyle.short)
        self.add_item(self.input)

    async def on_submit(self, itxn: discord.Interaction):
        emb = self.current_embed
        val = self.input.value
        if self.target == "Header": emb.set_author(name=val)
        elif self.target == "Title": emb.title = val
        elif self.target == "Body": emb.description = val
        elif self.target == "Footer": emb.set_footer(text=val)
        await itxn.response.edit_message(embed=emb)

class EmbedView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.embed = discord.Embed(title="Titel", description="Inhalt...", color=0xFFFFFF)

    @ui.button(label="Header", style=discord.ButtonStyle.gray)
    async def h_btn(self, itxn, b): await itxn.response.send_modal(TextModal("Header", self.embed))

    @ui.button(label="Titel", style=discord.ButtonStyle.gray)
    async def t_btn(self, itxn, b): await itxn.response.send_modal(TextModal("Title", self.embed))

    @ui.button(label="Text", style=discord.ButtonStyle.gray)
    async def b_btn(self, itxn, b): await itxn.response.send_modal(TextModal("Body", self.embed))

    @ui.button(label="Footer", style=discord.ButtonStyle.gray)
    async def f_btn(self, itxn, b): await itxn.response.send_modal(TextModal("Footer", self.embed))

    @ui.button(label="SENDEN", style=discord.ButtonStyle.green)
    async def send(self, itxn, b):
        await itxn.channel.send(embed=self.embed)
        await itxn.response.edit_message(content="✅ Gesendet", view=None, embed=None)

class EmbedBuilder(commands.Cog):
    def __init__(self, bot): self.bot = bot
    @app_commands.command(name="embed_builder", description="👷 Embed Builder")
    async def build(self, itxn: discord.Interaction):
        if not (itxn.user.guild_permissions.administrator or itxn.user.id in DEV_IDS):
            return await itxn.response.send_message("Denied.", ephemeral=True)
        await itxn.response.send_message(embed=discord.Embed(title="Editor Mode"), view=EmbedView(), ephemeral=True)

async def setup(bot): await bot.add_cog(EmbedBuilder(bot))