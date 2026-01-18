import discord, json, os
from discord.ext import commands
from discord import app_commands, ui

class ModmailActions(ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Beanspruchen", description="Du übernimmst den Support", emoji="👤"),
            discord.SelectOption(label="Schließen", description="Ticket beenden", emoji="🔒")
        ]
        super().__init__(placeholder="Aktion wählen...", options=options)

    async def callback(self, itxn: discord.Interaction):
        if self.values[0] == "Beanspruchen":
            await itxn.response.send_message(f"✅ {itxn.user.mention} bearbeitet jetzt diese Anfrage.")
        elif self.values[0] == "Schließen":
            await itxn.response.send_message("🔒 Ticket geschlossen.")
            await itxn.channel.edit(locked=True, archived=True)

class ModMail(commands.Cog):
    def __init__(self, bot):
        self.bot, self.path = bot, "modmail_config.json"

    @app_commands.command(name="modmail_setup", description="💌 Modmail System einrichten")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup(self, itxn: discord.Interaction, kanal: discord.TextChannel):
        with open(self.path, "w") as f: json.dump({str(itxn.guild_id): kanal.id}, f)
        await itxn.response.send_message(f"✅ Setup in {kanal.mention} eingerichtet.", ephemeral=False)

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot: return

        if not msg.guild: # User -> Bot
            if not os.path.exists(self.path): return
            with open(self.path, "r") as f: cfg = json.load(f)
            chan = self.bot.get_channel(list(cfg.values())[0])
            t_name = f"support-{msg.author.id}"
            thread = discord.utils.get(chan.threads, name=t_name)
            if not thread:
                thread = await chan.create_thread(name=t_name, type=discord.ChannelType.private_thread)
                v = ui.View(); v.add_item(ModmailActions())
                await thread.send(f"📩 Neue Mail von {msg.author.mention}", view=v)
            await thread.send(f"**User:** {msg.content}")

        elif isinstance(msg.channel, discord.Thread) and msg.channel.name.startswith("support-"):
            uid = int(msg.channel.name.split("-")[1])
            user = await self.bot.fetch_user(uid)
            await user.send(f"**Support:** {msg.content}")

async def setup(bot): await bot.add_cog(ModMail(bot))