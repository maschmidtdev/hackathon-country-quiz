import io
import json
import time
import urllib.parse
import urllib.request
import pygame


def play_hymn(country: str, infobox_data: dict, debug = False):
  country_cap = country.title()
  print(f"\n🔍 [AUDIO] Suche Hymne strikt über die Infobox für '{country_cap}'...")

  try:
    pygame.mixer.init()

    # 1. Hymnennamen strikt aus der Infobox auslesen
    anthem_name = None
    if infobox_data:
      for key, value in infobox_data.items():
        if "hymne" in key.lower():
          anthem_name = str(value).strip()
          break

    # 2. Suchanfragen basierend auf dem Infobox-Eintrag vorbereiten
    queries = []
    if anthem_name:
      if debug:
        print(f"📖 [AUDIO] Infobox-Hymnenname gefunden: '{anthem_name}'")
      queries.append(anthem_name)  # Höchste Priorität: Der exakte Name aus der Infobox

    # Fallbacks, falls die Infobox leer ist
    queries.append(f"Nationalhymne {country_cap}")
    queries.append(f"{country_cap} national anthem")

    file_title = None

    # 3. Datei anhand des Infobox-Namens suchen (Namensraum 6 = Mediendateien)
    for q in queries:
      search_url = f"https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(q)}&srnamespace=6&format=json"
      req = urllib.request.Request(search_url, headers={"User-Agent": "Mozilla/5.0"})
      data = json.loads(urllib.request.urlopen(req).read())
      results = data.get("query", {}).get("search", [])

      for res in results:
        title = res["title"]
        if any(ext in title.lower() for ext in ['.ogg', '.oga', '.mp3', '.flac']):
          file_title = title
          break
      if file_title:
        break

    if not file_title:
      if debug:
        print("❌ [AUDIO] Keine Audiodatei zur Infobox-Hymne gefunden.")
      return

    if debug:
      print(f"✅ [AUDIO] Ausgewählte Datei: {file_title}")

    # 4. CDN-URL abrufen und abspielen
    info_url = f"https://commons.wikimedia.org/w/api.php?action=query&titles={urllib.parse.quote(file_title)}&prop=imageinfo&iiprop=url&format=json"
    info_req = urllib.request.Request(info_url, headers={"User-Agent": "Mozilla/5.0"})
    info_data = json.loads(urllib.request.urlopen(info_req).read())

    info_pages = info_data.get("query", {}).get("pages", {})
    audio_url = next(
        (
            page["imageinfo"][0]["url"]
            for page in info_pages.values()
            if "imageinfo" in page
        ),
        None,
    )

    if not audio_url:
      if debug:
        print("❌ [AUDIO] Konnte die Download-URL nicht auflösen.")
      return

    audio_url = audio_url.split("?")[0]
    if audio_url.startswith("//"):
      audio_url = "https:" + audio_url

    if debug:
      print(f"📥 [AUDIO] Lade Audio von: {audio_url}")
    audio_bytes = urllib.request.urlopen(
        urllib.request.Request(audio_url, headers={"User-Agent": "Mozilla/5.0"})
    ).read()

    ext = "ogg" if audio_url.lower().endswith((".ogg", ".oga")) else "mp3"
    pygame.mixer.music.load(io.BytesIO(audio_bytes), namehint=ext)
    pygame.mixer.music.play()

    print("🎵 [AUDIO] Wiedergabe läuft (10 Sekunden)...")
    time.sleep(10)
    pygame.mixer.music.stop()
    print("✅ [AUDIO] Fertig!")

  except Exception as e:
    print(f"❌ [AUDIO] Fehler aufgetreten: {e}")



def main():
  # Testen
  play_hymn("Deutschland")

if __name__ == '__main__':
    main()
