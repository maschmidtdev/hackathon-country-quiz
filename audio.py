import io
import json
import time
import urllib.request
import urllib.parse
import pygame

pygame.mixer.init()

def play_hymn(country: str):
    print(f"🔍 Suche Hymne für {country}...")
    
    # 1. Im Datei-Namespace nach der Nationalhymne des Landes suchen
    search_query = f"Nationalhymne {country}"
    search_url = f"https://de.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(search_query)}&srnamespace=6&format=json"
    
    req = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        data = json.loads(urllib.request.urlopen(req).read())
        results = data.get("query", {}).get("search", [])
        
        # Erste passende Audiodatei finden
        file_title = next((item['title'] for item in results if item['title'].lower().endswith(('.ogg', '.oga', '.mp3'))), None)
        
        if not file_title:
            print("❌ Keine Audiodatei auf Wikipedia gefunden.")
            return
            
        # 2. Direkte CDN-URL für den Dateinamen abfragen
        info_url = f"https://de.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(file_title)}&prop=imageinfo&iiprop=url&format=json"
        info_req = urllib.request.Request(info_url, headers={'User-Agent': 'Mozilla/5.0'})
        info_data = json.loads(urllib.request.urlopen(info_req).read())
        
        pages = info_data.get("query", {}).get("pages", {})
        audio_url = next((page['imageinfo'][0]['url'] for page in pages.values() if 'imageinfo' in page), None)
        
        if not audio_url:
            print("❌ Konnte Download-URL nicht abrufen.")
            return
            
        # Parameter bereinigen
        audio_url = audio_url.split('?')[0]
        if audio_url.startswith("//"):
            audio_url = "https:" + audio_url
            
        # 3. Audio herunterladen und im RAM abspielen
        print("📥 Lade Audio...")
        audio_bytes = urllib.request.urlopen(urllib.request.Request(audio_url, headers={'User-Agent': 'Mozilla/5.0'})).read()
        
        ext = "ogg" if audio_url.lower().endswith(('.ogg', '.oga')) else "mp3"
        pygame.mixer.music.load(io.BytesIO(audio_bytes), namehint=ext)
        pygame.mixer.music.play()
        
        print("🎵 Wiedergabe läuft (5 Sekunden)...")
        time.sleep(5)
        pygame.mixer.music.stop()
        print("✅ Fertig!")
        
    except Exception as e:
        print(f"❌ Fehler: {e}")

# Testen
play_hymn("Deutschland")