import discord, calendar, json, os
from discord.ext import commands
from discord import app_commands
from datetime import datetime

class CalendarView(discord.ui.View):
    def __init__(self, cog, month, year):
        super().__init__(timeout=60)
        self.cog, self.month, self.year = cog, month, year

    async def update_view(self, itxn):
        if self.month < 1: self.month, self.year = 12, self.year - 1
        elif self.month > 12: self.month, self.year = 1, self.year + 1
        await itxn.response.edit_message(embed=self.cog.create_cal(self.month, self.year), view=self)

    @discord.ui.button(label="◀", style=discord.ButtonStyle.gray)
    async def prev(self, itxn, btn):
        self.month -= 1
        await self.update_view(itxn)

    @discord.ui.button(label="▶", style=discord.ButtonStyle.gray)
    async def next(self, itxn, btn):
        self.month += 1
        await self.update_view(itxn)

class CalendarBot(commands.Cog):
    def __init__(self, bot): self.bot = bot

    def create_cal(self, month, year):
        cal = calendar.monthcalendar(year, month)
        data = json.load(open("birthdays.json")) if os.path.exists("birthdays.json") else {}
        bdays = [int(v['date'].split('.')[0]) for v in data.values() if int(v['date'].split('.')[1]) == month]

        lines = ["MO  DI  MI  DO  FR  SA  SO", "──" * 13]
        for week in cal:
            line = ""
            for d in week:
                if d == 0: line += "    "
                else: line += f"{d:02} " + ("🎂" if d in bdays else " ")
            lines.append(line)

        m_names = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
        return discord.Embed(title=f"📅 {m_names[month-1]} {year}", description=f"```\n" + "\n".join(lines) + "\n```", color=0xFFFFFF)

    @app_commands.command(name="calendar", description="📅 Öffnet den interaktiven Kalender")
    async def show_cal(self, itxn: discord.Interaction):
        now = datetime.now()
        await itxn.response.send_message(embed=self.create_cal(now.month, now.year), view=CalendarView(self, now.month, now.year))

async def setup(bot): await bot.add_cog(CalendarBot(bot))