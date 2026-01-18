import discord, os, asyncio
from discord.ext import commands

class MyBot(commands.AutoShardedBot):
    def __init__(self):
        intents = discord.Intents.all()
        # Shard-Anzahl wird automatisch von Discord verwaltet
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Lädt alle Cogs aus dem Ordner
        for f in os.listdir("./cogs"):
            if f.endswith(".py"):
                await self.load_extension(f"cogs.{f[:-3]}")
                print(f"Geladen: {f}")

        # Synchronisiert Slash-Befehle global
        await self.tree.sync()
        print("Slash-Befehle synchronisiert!")

    async def on_ready(self):
        print(f"Eingeloggt als {self.user} (ID: {self.user.id})")
        await self.change_presence(
            activity=discord.CustomActivity(name="🧑‍💻 Print Hello World.")
        )

bot = MyBot()
token = os.getenv("DISCORD_TOKEN")
bot.run(token)