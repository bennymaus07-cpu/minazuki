import discord, json, os, re
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Select, Modal, TextInput

OWNER_IDS = [1461462642626396375] # Deine ID

def get_db():
    if os.path.exists("birthdays.json"):
        with open("birthdays.json", "r") as f: return json.load(f)
    return {}

def save_db(data):
    with open("birthdays.json", "w") as f: json.dump(data, f, indent=4)

def build_pro_embed():
    data = get_db()
    months = {
        "01": "Januar🎂", "02": "Februar🎂", "03": "März🎂", "04": "April🎂",
        "05": "Mai🎂", "06": "Juni🎂", "07": "Juli🎂", "08": "August🎂",
        "09": "September🎂", "10": "Oktober🎂", "11": "November🎂", "12": "Dezember🎂"
    }

    desc = "🗓️ **Geburtstags-Datenbank**\n*Verwalte die Ehrentage der Mitglieder.*\n\n"
    found = False

    for m_num, m_name in months.items():
        entries = []
        for name, info in sorted(data.items(), key=lambda x: x[1]['date']):
            d, m = info['date'].split('.')
            if m == m_num:
                age = f" • wird **{2026-int(info['year'])}**" if info['year'].isdigit() else ""
                entries.append(f"📅 **{d}. {m_name}** — {name}{age}")

        if entries:
            found = True
            desc += f"# {m_name}\n" + "\n".join(entries) + "\n\n"

    if not found: desc += "> *Keine Einträge vorhanden.*"
    return discord.Embed(description=desc, color=0xFFFFFF)

class AddModal(Modal, title="Registrierung"):
    name = TextInput(label="Name", placeholder="Benny")
    date = TextInput(label="Datum (TT.MM)", placeholder="16.05")
    year = TextInput(label="Jahr (Optional)", required=False)
    async def on_submit(self, itxn: discord.Interaction):
        if not re.match(r"^\d{2}\.\d{2}$", str(self.date)):
            return await itxn.response.send_message("Format: TT.MM!", ephemeral=True)
        data = get_db()
        data[str(self.name)] = {"date": str(self.date), "year": str(self.year) or "N/A"}
        save_db(data)
        await itxn.response.edit_message(embed=build_pro_embed())

class DelModal(Modal, title="Entfernen"):
    name = TextInput(label="Name")
    async def on_submit(self, itxn: discord.Interaction):
        data = get_db()
        if data.pop(str(self.name), None):
            save_db(data); await itxn.response.edit_message(embed=build_pro_embed())
        else: await itxn.response.send_message("Nicht gefunden!", ephemeral=True)

class BDayView(View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.select(placeholder="Option wählen...", options=[
        discord.SelectOption(label="Eintragen", value="add", emoji="🎂"),
        discord.SelectOption(label="Löschen", value="del", emoji="🗑️")
    ])
    async def action(self, itxn: discord.Interaction, select: Select):
        if select.values[0] == "add": await itxn.response.send_modal(AddModal())
        elif itxn.user.id in OWNER_IDS: await itxn.response.send_modal(DelModal())
        else: await itxn.response.send_message("📛 Zugriff verweigert! Du bist kein Entwickler von diesem Bot.", ephemeral=True)

class Birthdays(commands.Cog):
    def __init__(self, bot): self.bot = bot
    @app_commands.command(name="birthday", description="🎁 Geburtstags Panel")
    async def b_admin(self, itxn: discord.Interaction):
        await itxn.response.send_message(embed=build_pro_embed(), view=BDayView())

async def setup(bot): await bot.add_cog(Birthdays(bot))