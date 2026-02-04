import discord
from discord.ext import commands
import os
import requests
from bs4 import BeautifulSoup

# --- KONFIGURATION ---
# Wir holen den Token sicher aus Koyeb (Environment Variables)
TOKEN = os.getenv('DISCORD_TOKEN')
TARGET_USER_ID = 1396141315959296233 

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

def get_weed_info():
    """Holt aktuelle Infos von weedseedexpress.com"""
    try:
        url = "https://weedseedexpress.com"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Beispiel: Holt den Titel der Seite oder erste Angebote
            # Du kannst die Selektoren anpassen, je nachdem was genau du suchst
            title = soup.title.string if soup.title else "Kein Titel gefunden"
            return f"Infos von Weedseedexpress: {title}"
        else:
            return "Fehler: Webseite nicht erreichbar."
    except Exception as e:
        return f"Scraping-Fehler: {str(e)}"

@bot.event
async def on_ready():
    print(f'-----------------------------------')
    print(f'omamilch V5 ist ONLINE')
    print(f'-----------------------------------')
    
    # Sendet Start-Info und die Webseiten-Daten an dich
    user = await bot.fetch_user(TARGET_USER_ID)
    if user:
        info = get_weed_info()
        await user.send(f"Bin Jetzt verfügbar!\n\n{info}")

@bot.command()
async def check(ctx):
    """Befehl um manuell die Infos abzurufen"""
    await ctx.send("Rufe Daten ab...")
    info = get_weed_info()
    await ctx.send(info)

# Startet den Bot sicher
if TOKEN:
    bot.run(TOKEN)
else:
    print("FEHLER: DISCORD_TOKEN nicht in Koyeb hinterlegt!")
    
