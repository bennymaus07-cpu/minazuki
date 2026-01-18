import discord
from discord.ext import commands
from discord import app_commands, components
from discord.ui import Select, View

class ProfileSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="River", description="Infos über river", emoji="🤍"),
            discord.SelectOption(label="Hedi", description="Infos über Hedi", emoji="🖤"),
            discord.SelectOption(label="minazuki", description="Infos über minazuki", emoji="🛡️"),
            discord.SelectOption(label="Emilia", description="Infos über Emilia", emoji="💅"),
            discord.SelectOption(label="Felix", description="Infos über Felix", emoji="❄️")

            ]
        super().__init__(placeholder="Wähle ein Profil aus...", options=options)

    async def callback(self, itxn: discord.Interaction):
        if self.values[0] == "River":
            embed = discord.Embed(title="Profil von River", color=0xFFFFFF)
            embed.add_field(name="Name", value="river", inline=True)
            embed.add_field(name="Alter", value="17", inline=True)
            embed.add_field(name="Farbe", value="Weiß", inline=True)
            embed.add_field(name="Hobbys", value="Programmieren, Musik Hören, Nerven, Chille, Zocken", inline=True)
            embed.add_field(name="Lieblings Film", value="Hat Kein Lieblings Film.", inline=True)
            embed.add_field(name="Lieblings Serie", value="Hat Keine Lieblings Serie.", inline=True)
            embed.add_field(name="Lieblings Spiel", value="Minecraft, Fortnite", inline=True)
            embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1461998972452475046/a2305ed0fccbda0424b65f2c8584e1f4.webp?size=128")
            embed.set_footer(text="Bot Entwickler")

        elif self.values[0] == "Hedi":
            embed = discord.Embed(title="Profil von Hedi", color=0x0C0000)
            embed.add_field(name="Name", value="Hedi", inline=True)
            embed.add_field(name="Alter", value="16", inline=True)
            embed.add_field(name="Farbe", value="Schwarz", inline=True)
            embed.add_field(name="Hobbys", value="Programmieren, Musik Hören, Chillen, Schlafen, Trinken, Essen, Sprechen", inline=True)
            embed.add_field(name="Lieblins Fim", value="Fear Below", inline=True)
            embed.add_field(name="Lieblings Serie", value="Welcome to Derry", inline=True)
            embed.add_field(name="Lieblings Spiel", value="Roblox, Minecraft", inline=True)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1461465821070233714/1461761196800606279/anonymous-che-guevara-61629-large.jpg?ex=696c6373&is=696b11f3&hm=6d345fc1fe1ac033b8cdce9d450af0df0c020eb8af54f59b8564e867ab5d6616&")
            embed.set_footer(text="Bot Entwickler")

        elif self.values[0] == "minazuki":
             embed = discord.Embed(title="Profil von minazuki", color=0xc0c26a)
             embed.add_field(name="Name", value="minazuki", inline=True)
             embed.add_field(name="Alter", value="16", inline=True)
             embed.add_field(name="Farbe", value="Grün", inline=True)
             embed.add_field(name="Hobbys", value="Programmieren, Musik Hören, Zocken", inline=True)
             embed.add_field(name="Lieblins Fim", value="M3GAN", inline=True)
             embed.add_field(name="Lieblings Serie", value="The Rookie", inline=True)
             embed.add_field(name="Lieblings Spiel", value="Roblox, Minecraft", inline=True)
             embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1461462642626396375/1ed816df8f5304585c55f540cd04059a.webp?size=128")
             embed.set_footer(text="Bot Owner")

        elif self.values[0] == "Emilia":
         embed = discord.Embed(title="Profil von Emilia", color=0x52399c)
         embed.add_field(name="Name", value="Emilia", inline=True)
         embed.add_field(name="Alter", value="15", inline=True)
         embed.add_field(name="Farbe", value="Lila", inline=True)
         embed.add_field(name="Hobbys", value="Kochen und Zeichnen", inline=True)
         embed.add_field(name="Lieblins Fim", value="/", inline=True)
         embed.add_field(name="Lieblings Serie", value="The Rookie", inline=True)
         embed.add_field(name="Lieblings Spiel", value="Roblox", inline=True)
         embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1456339754739171400/3799a46ff92ffa2352a71b6f9d0e0a9a.webp?size=128")
         embed.set_footer(text="Server Mitglied")

        elif self.values[0] == "Felix":
         embed = discord.Embed(title="Profil von Felix", color=0x0C0000)
         embed.add_field(name="Name", value="Felix", inline=True)
         embed.add_field(name="Alter", value="15", inline=True)
         embed.add_field(name="Farbe", value="Rot", inline=True)
         embed.add_field(name="Hobbys", value="Zocken und an Autos basteln", inline=True)
         embed.add_field(name="Lieblins Fim", value="/", inline=True)
         embed.add_field(name="Lieblings Serie", value="The Watcher", inline=True)
         embed.add_field(name="Lieblings Spiel", value="Brawl Stars", inline=True)
         embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1417916922883997778/33f27e7a8bbcbe5ebf2b7c437e081378.webp?size=128")
         embed.set_footer(text="Server")
             

        await itxn.response.edit_message(embed=embed)

class ProfileView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ProfileSelect())

class Profiles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="user_info", description="🪧 Zeigt die Team-Profile")
    async def user_info(self, itxn: discord.Interaction):
        # Liste der Namen für die Statistik (kannst du erweitern)
        members = ["river", "Hedi", "minazuki", "Emilia", "Felix"]

        embed = discord.Embed(
            title="📇 Mitglieder-Verzeichnis",
            description=(
                "Willkommen im Verzeichnis! Hier findest du alle "
                "Hintergrundinfos zu unseren Teammitgliedern.\n\n"
                "**Anleitung:**\n"
                "Wähle unten im Menü ein Mitglied aus, um dessen "
                "vollständiges Profil mit Hobbys und Favoriten zu laden."
            ),
            color=0x2b2d31
        )

        embed.add_field(
            name="📊 Statistik", 
            value=f"Aktuell sind **{len(members)}** Profile hinterlegt.", 
            inline=False
        )
        embed.add_field(
            name="👥 Gelistete Mitglieder", 
            value="\n".join([f"• {m}" for m in members]), 
            inline=False
        )

        embed.set_footer(text="System online • Wähle ein Profil")

        await itxn.response.send_message(embed=embed, view=ProfileView())


    @app_commands.command(name="server_info", description="📊 Zeigt Server Infos")
    async def server_info(self, itxn: discord.Interaction):
        guild = itxn.guild
        embed = discord.Embed(title="📊Server Info", color=0x2b2d31)
        embed.add_field(name="🪪Name", value=guild.name, inline=True)
        embed.add_field(name="🆔ID", value=guild.id, inline=True)
        embed.add_field(name="👥Gesamt", value=guild.member_count, inline=True)
        embed.add_field(name="📅Erstellt am", value=guild.created_at.strftime("%d.%m.%Y"), inline=True)
        embed.add_field(name="👑Besitzer", value=guild.owner.mention, inline=True)
        embed.add_field(name="💬Kanäle", value=len(guild.channels), inline=True)
        embed.add_field(name="🎭Rollen", value=len(guild.roles), inline=True)
        embed.add_field(name="🌍Region", value=guild.preferred_locale, inline=True)
        embed.add_field(name="🔒Verifizierungsstufe", value=guild.verification_level, inline=True)
        embed.add_field(name="📌AFK-Kanal", value=guild.afk_channel.mention if guild.afk_channel else "Kein AFK-Kanal", inline=True)
        embed.add_field(name="🎵AFK-Timeout", value=f"{guild.afk_timeout/60} Minuten", inline=True)
        embed.add_field(name="🍋‍🟩System-Kanal", value=guild.system_channel.mention if guild.system_channel else "Kein System-Kanal", inline=True)
        embed.add_field(name="📋Regeln-Kanal", value=guild.rules_channel.mention if guild.rules_channel else "Kein Regeln-Kanal", inline=True)
        embed.add_field(name="🤖Bots", value=sum(1 for member in guild.members if member.bot), inline=True)
        embed.add_field(name="👥Menschen", value=sum(1 for member in guild.members if not member.bot), inline=True)
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        await itxn.response.send_message(embed=embed)
        

async def setup(bot):
    await bot.add_cog(Profiles(bot))