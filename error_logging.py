import discord, traceback, datetime
from discord.ext import commands

class ErrorCenter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.error_log_id = 1462394102225043652  # Deine Channel-ID

    @commands.Cog.listener()
    async def on_app_command_error(self, itxn: discord.Interaction, error: Exception):
        # Fehler-Details extrahieren
        error_msg = "".join(traceback.format_exception(type(error), error, error.__traceback__))

        emb = discord.Embed(
            title="⚠️ Command Error",
            description=f"**Command:** `/{itxn.command.name}`\n**User:** {itxn.user} (`{itxn.user.id}`)",
            color=0xff4444,
            timestamp=datetime.datetime.now()
        )
        # Den Traceback in einen Codeblock packen (gekürzt auf 1000 Zeichen)
        emb.add_field(name="Traceback", value=f"```py\n{error_msg[:1000]}```", inline=False)

        log_ch = self.bot.get_channel(self.error_log_id)
        if log_ch: await log_ch.send(embed=emb)

        # User-Feedback
        if not itxn.response.is_done():
            await itxn.response.send_message("❌ Interner Fehler wurde gemeldet.", ephemeral=True)

async def setup(bot): await bot.add_cog(ErrorCenter(bot))