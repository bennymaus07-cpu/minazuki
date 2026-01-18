import discord
from discord.ext import commands
from discord import app_commands

class PanicSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.maintenance = False  # Globaler Status

    @app_commands.command(name="panic", description="🚨 Schaltet den Wartungsmodus ein/aus")
    async def panic(self, itxn: discord.Interaction):
        if not await self.bot.is_owner(itxn.user): return

        self.bot.maintenance = not self.bot.maintenance
        status = "AKTIVIERT 🔴" if self.bot.maintenance else "DEAKTIVIERT 🟢"

        await itxn.response.send_message(f"⚠️ Wartungsmodus {status}. Nur Owner können Befehle nutzen.", ephemeral=True)

    # Der Wächter: Prüft JEDEN Befehl vor der Ausführung
    async def interaction_check(self, itxn: discord.Interaction):
        if self.bot.maintenance and not await self.bot.is_owner(itxn.user):
            await itxn.response.send_message("🛠️ **Wartung:** Der Bot wird gerade repariert. Bitte warte kurz.", ephemeral=True)
            return False
        return True



class InviteTracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.invites = {} # Cache für Invites

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            try: self.invites[guild.id] = await guild.invites()
            except: pass

    @commands.Cog.listener()
    async def on_member_join(self, member):
        invites_before = self.invites.get(member.guild.id, [])
        invites_after = await member.guild.invites()

        for invite in invites_before:
            for after in invites_after:
                if invite.code == after.code and after.uses > invite.uses:
                    # HIER LOGGEN
                    print(f"{member} kam via {invite.inviter} (Code: {invite.code})")
        self.invites[member.guild.id] = invites_after


    @app_commands.command(name="guild_admin", description="Verwaltet alle Server des Bots")
    async def guild_admin(self, itxn: discord.Interaction):
        if not await self.bot.is_owner(itxn.user): return

        guilds = sorted(self.bot.guilds, key=lambda g: g.member_count, reverse=True)[:10]
        msg = "**Top 10 Server:**\n"
        for g in guilds:
            msg += f"• `{g.id}` | **{g.name}** ({g.member_count} User)\n"

        await itxn.response.send_message(msg, ephemeral=True)

    @app_commands.command(name="shards", description="Status aller Shards prüfen")
    async def shards(self, itxn: discord.Interaction):
        if not await self.bot.is_owner(itxn.user): return

        msg = "🛰️ **Shard Status:**\n"
        for shard_id, shard in self.bot.shards.items():
            status = "🟢" if not shard.is_closed() else "🔴"
            msg += f"Shard `{shard_id}`: {status} | `{round(shard.latency * 1000)}ms`\n"

        await itxn.response.send_message(msg, ephemeral=True)




    @app_commands.command(name="check_perms", description="Prüft Bot-Rechte auf diesem Server")
    async def check_perms(self, itxn: discord.Interaction):
        p = itxn.guild.me.guild_permissions
        perms = {
            "Administrator": p.administrator,
            "Nachrichten senden": p.send_messages,
            "Embeds einbetten": p.embed_links,
            "Dateien anhängen": p.attach_files,
            "Reaktionen hinzufügen": p.add_reactions,
            "External Emojis": p.external_emojis
        }

        status = "\n".join([f"{'✅' if v else '❌'} {k}" for k, v in perms.items()])
        emb = discord.Embed(title="🛡️ Permission Check", description=status, color=0x5865F2)
        await itxn.response.send_message(embed=emb, ephemeral=True)


    @app_commands.command(name="clean_invites", description="🧯 Löscht alle vom Bot erstellten Invites")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def clean_invites(self, itxn: discord.Interaction):
        invites = await itxn.guild.invites()
        deleted = 0
        for inv in invites:
            if inv.inviter.id == self.bot.user.id:
                await inv.delete()
                deleted += 1
        await itxn.response.send_message(f"🧹 `{deleted}` Invites gelöscht!", ephemeral=True)


    @app_commands.command(name="find_user", description="Zeigt gemeinsame Server mit einem User")
    async def find_user(self, itxn: discord.Interaction, user_id: str):
        if not await self.bot.is_owner(itxn.user): return

        target = self.bot.get_user(int(user_id))
        if not target: return await itxn.response.send_message("❌ User nicht gefunden.")

        mutuals = [g.name for g in target.mutual_guilds]
        msg = f"👤 **{target}** ist auf {len(mutuals)} gemeinsamen Servern:\n" + "\n".join(f"• {name}" for name in mutuals[:15])

        await itxn.response.send_message(msg, ephemeral=True)


async def setup(bot): await bot.add_cog(PanicSystem(bot))