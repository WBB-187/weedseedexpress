import discord
from discord.ext import tasks
import requests
from bs4 import BeautifulSoup
import asyncio

# --- MTQ2ODU0ODE1NzgxNzQ4NzQwNQ.G3J0qA.nBhpQIlmWGln6WPGFGfTqKPOzLLRzYqUhUlHwU ---
TOKEN = 'DEIN_BOT_TOKEN_HIER'
USER_ID = 1396141315959296233
URL = 'https://weedseedexpress.com/de/angebote'
KEY = 'HanfmomentV1'
# ---------------------

class PromoBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_deals = set()

    async def setup_hook(self):
        self.check_website.start()

    async def on_ready(self):
        print(f'-----------------------------------')
        print(f'omamilch V5 ist ONLINE')
        print(f'Ziel-ID: {USER_ID}')
        print(f'-----------------------------------')
        
        # Sofort-Nachricht beim Start
        user = await self.fetch_user(USER_ID)
        await user.send(f"✅ **omamilch V5 Einsatzbereit!**\nSende dir jetzt alle aktuellen Angebote von weedseedexpress.com...")
        
        # Erster Full-Scan sofort beim Start
        await self.scrape_and_send()

    @tasks.loop(minutes=60)
    async def check_website(self):
        print("[INFO] Stündlicher Check läuft...")
        await self.scrape_and_send()

    async def scrape_and_send(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }
        try:
            response = requests.get(URL, headers=headers, timeout=20)
            if response.status_code != 200:
                print(f"[FEHLER] Seite nicht erreichbar. Status: {response.status_code}")
                return

            soup = BeautifulSoup(response.text, 'html.parser')
            # Suche nach den Produkt-Karten auf der Seite
            products = soup.find_all('li', class_='item product product-item')
            
            user = await self.fetch_user(USER_ID)
            new_count = 0

            for product in products:
                try:
                    name_tag = product.find('a', class_='product-item-link')
                    name = name_tag.get_text(strip=True)
                    link = name_tag['href']
                    
                    # Bild extrahieren
                    img_tag = product.find('img', class_='product-image-photo')
                    img_url = img_tag['data-src'] if img_tag and img_tag.has_attr('data-src') else (img_tag['src'] if img_tag else "")

                    # Preis extrahieren
                    price_tag = product.find('span', class_='price')
                    price = price_tag.get_text(strip=True) if price_tag else "Preis auf Anfrage"

                    if name not in self.last_deals:
                        embed = discord.Embed(
                            title=name,
                            url=link,
                            color=discord.Color.dark_green(),
                            description=f"💰 **Aktuelles Angebot:** {price}"
                        )
                        if img_url:
                            embed.set_image(url=img_url)
                        
                        embed.set_footer(text=f"Partnerschaft Update | {KEY}")
                        
                        await user.send(embed=embed)
                        self.last_deals.add(name)
                        new_count += 1
                        # Kleiner Delay, um Discord-Rate-Limits zu vermeiden
                        await asyncio.sleep(1) 
                except Exception as inner_e:
                    continue

            print(f"[INFO] Scan abgeschlossen. {new_count} neue Angebote gesendet.")

        except Exception as e:
            print(f"[FEHLER] Netzwerk-Problem: {e}")

intents = discord.Intents.default()
intents.members = True 
client = PromoBot(intents=intents)
client.run(TOKEN)
