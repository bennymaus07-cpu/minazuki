import discord, io, textwrap, contextlib, psutil, platform
from discord.ext import commands
from discord import app_commands
class Developer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, itxn: discord.Interaction):
        return await self.bot.is_owner(itxn.user)

    @app_commands.command(name="broadcast", description="📯 Sendet eine Nachricht an alle Server")
    async def broadcast(self, itxn: discord.Interaction, msg: str):
        await itxn.response.send_message("📢 Sende...", ephemeral=True)
        count = 0
        for g in self.bot.guilds:
            ch = next((c for c in g.text_channels if c.permissions_for(g.me).send_messages), None)
            if ch:
                try: 
                    await ch.send(f"⚠️ **Update:** {msg}")
                    count += 1
                except: continue
        await itxn.followup.send(f"✅ An {count} Server gesendet.")

    @app_commands.command(name="eval", description="💻 Führt Python Code aus")
    async def eval_code(self, itxn: discord.Interaction, code: str):
        await itxn.response.defer()
        out = io.StringIO()
        env = {'bot': self.bot, 'itxn': itxn, 'ch': itxn.channel}
        try:
            with contextlib.redirect_stdout(out):
                exec(f"async def f():\n{textwrap.indent(code, '    ')}", env)
                await env['f']()
            res = out.getvalue() or "Erfolg!"
        except Exception as e: res = str(e)
        await itxn.followup.send(f"```py\n{res[:1900]}```")

    @app_commands.command(name="sysinfo", description="🖥️ Zeigt System Infos")
    async def sysinfo(self, itxn: discord.Interaction):
        emb = discord.Embed(title="🖥️ Status", color=0x00ff00)
        emb.add_field(name="RAM", value=f"{psutil.virtual_memory().percent}%")
        emb.add_field(name="Ping", value=f"{round(self.bot.latency * 1000)}ms")
        await itxn.response.send_message(embed=emb)


    @app_commands.command(name="leaveserver", description="🚪 Lässt den Bot einen Server verlassen (Owner only)")
    async def leave_server(self, itxn: discord.Interaction, server_id: str):
        if not await self.bot.is_owner(itxn.user):
            return await itxn.response.send_message("❌ Nur für den Developer!", ephemeral=True)

        guild = self.bot.get_guild(int(server_id))
        if not guild:
            return await itxn.response.send_message("❌ Server nicht gefunden.", ephemeral=True)

        await guild.leave()
        await itxn.response.send_message(f"✅ Server **{guild.name}** ({server_id}) wurde verlassen.")

    

    @app_commands.command(name="serverlist", description="📋 Listet alle Server auf (Owner only)")
    async def server_list(self, itxn: discord.Interaction):
        if not await self.bot.is_owner(itxn.user):
            return await itxn.response.send_message("❌ Zugriff verweigert.", ephemeral=True)

        # Erstellt eine Liste: "Name (ID) - Member"
        list_str = "\n".join([f"• **{g.name}** (`{g.id}`) - {g.member_count} User" for g in self.bot.guilds])

        embed = discord.Embed(title="🌐 Aktive Server", description=list_str or "Keine Server gefunden.", color=0x3498db)
        await itxn.response.send_message(embed=embed, ephemeral=True)



    @app_commands.command(name="backup", description="📝 Sendet die Datenbank-Datei (Owner only)")
    async def backup(self, itxn: discord.Interaction):
        if not await self.bot.is_owner(itxn.user):
            return await itxn.response.send_message("❌ Kein Zugriff.", ephemeral=True)

        file_path = "database.json" # Hier den Namen deiner Datei anpassen!

        if os.path.exists(file_path):
            file = discord.File(file_path)
            await itxn.response.send_message("📦 Hier ist dein Datenbank-Backup:", file=file, ephemeral=True)
        else:
            await itxn.response.send_message("❌ Datei nicht gefunden.", ephemeral=True)



async def setup(bot): await bot.add_cog(Developer(bot))