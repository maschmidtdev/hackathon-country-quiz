import io
import json
import random
import urllib.parse
import urllib.request
import miniaudio
import requests
from infobox import fetch_infobox_data

# Globale Variable für das Miniaudio-Gerät (zum Stoppen des Sounds)
current_audio_device = None

countries = ["Deutschland", "Frankreich", "Spanien", "Italien", "Namibia"]

info_difficulty = {
    "ignore": [
        "Errichtung",
        "Internet-TLD",
        "Vorgängergebilde",
        "ISO 3166",
        "Nationalfeiertag"
    ],
    "schwer": [
        "Wahlsprache",
        "Amtssprache",
        "Telefonvorwahl",
        "Staats- und Regierungsform",
        "Bevölkerungsdichte",
        "Parlament(e)",
        "Bevölkerungsentwicklung",
        "BruttoinlandsproduktTotal (nominal)Total (KKP)BIP/Einw. (nom.)BIP/Einw. (KKP)",
        "Index der menschlichen Entwicklung(HDI)"
    ],
    "mittel": [
        "Staatsoberhaupt",
        "Staatsreligion",
        "Fläche",
        "Regierungschef",
        "Regierung",
        "Einwohnerzahl",
        "Währung"
    ],
    "leicht": [
        "Zeitzone",
        "Kfz-Kennzeichen",
        "Hauptstadt",
        "Nationalhymne"
    ]
}

infobox_data = {}

difficulty_counts = {
    "schwer": 2,
    "mittel": 3,
    "leicht": 2
}


def play_hymn(country: str):
    """Sucht die Nationalhymne zuverlässig über die Wikipedia-API und spielt sie mit miniaudio im RAM ab."""
    global current_audio_device
    stop_hymn()

    try:
        # 1. Im Datei-Namespace nach der Nationalhymne des Landes suchen
        search_query = f"Nationalhymne {country}"
        search_url = f"https://de.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(search_query)}&srnamespace=6&format=json"
        
        req = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0'})
        data = json.loads(urllib.request.urlopen(req).read())
        results = data.get("query", {}).get("search", [])
        
        file_title = next((item['title'] for item in results if item['title'].lower().endswith(('.ogg', '.oga', '.mp3'))), None)
        
        if not file_title:
            print("[Keine Audiodatei auf Wikipedia gefunden]")
            return
            
        # 2. Direkte CDN-URL abfragen
        info_url = f"https://de.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(file_title)}&prop=imageinfo&iiprop=url&format=json"
        info_req = urllib.request.Request(info_url, headers={'User-Agent': 'Mozilla/5.0'})
        info_data = json.loads(urllib.request.urlopen(info_req).read())
        
        pages = info_data.get("query", {}).get("pages", {})
        audio_url = next((page['imageinfo'][0]['url'] for page in pages.values() if 'imageinfo' in page), None)
        
        if not audio_url:
            print("[Konnte Download-URL nicht abrufen]")
            return
            
        audio_url = audio_url.split('?')[0]
        if audio_url.startswith("//"):
            audio_url = "https:" + audio_url
            
        # 3. Audio-Daten herunterladen und mit miniaudio abspielen
        audio_bytes = urllib.request.urlopen(urllib.request.Request(audio_url, headers={'User-Agent': 'Mozilla/5.0'})).read()
        
        fmt = miniaudio.FileFormat.MP3 if audio_url.lower().endswith('.mp3') else miniaudio.FileFormat.OGG
        stream = miniaudio.stream_any(audio_bytes, fmt)
        
        current_audio_device = miniaudio.PlaybackDevice()
        current_audio_device.start(stream)
        print("🎵 [Spiele Nationalhymne im Terminal ab...]")

    except Exception as e:
        print(f"[Fehler beim Abspielen der Audio-Datei: {e}]")


def stop_hymn():
    """Stoppt die Audiowiedergabe, falls sie läuft."""
    global current_audio_device
    if current_audio_device:
        try:
            current_audio_device.close()
        except Exception:
            pass
        current_audio_device = None


def get_random_info(difficulty, country) -> str:
    if len(info_difficulty[difficulty]) == 0:
        return ""

    info = random.choice(info_difficulty[difficulty])
    info_difficulty[difficulty].remove(info)

    if info in infobox_data:
        # Falls der Hinweis "Nationalhymne" ist, spiele den Ton ab
        if info == "Nationalhymne":
            play_hymn(country)
            
        return f"{info}: {infobox_data[info]}"
    else:
        return get_random_info(difficulty, country)


def get_country_from_user() -> str:
    guess = input("Auf welches Land tippst du?: ").strip()

    if not guess:
        print("Eingabe ungültig, erneute Eingabe:")
        return get_country_from_user()

    return guess


def play_game(difficulties, country) -> int:
    score = len(difficulties)

    for difficulty in difficulties:
        random_info = get_random_info(difficulty, country)

        if not random_info:
            score -= 1
            continue

        print(random_info)
        guess = get_country_from_user()

        if country.lower() == guess.lower():
            stop_hymn()
            return score
        else:
            stop_hymn()
            score -= 1

    stop_hymn()
    return score


def get_difficulties() -> list:
    difficulties = []
    for key, value in difficulty_counts.items():
        for i in range(value):
            difficulties.append(key)
    return difficulties


def print_missing_info(infobox_data, info_difficulty):
    missing = list(infobox_data.keys())

    for info in infobox_data:
        for key, infolist in info_difficulty.items():
            if key == "ignore":
                continue

            if info in infolist:
                if info in missing:
                    missing.remove(info)
                break

    print("\nMissing infos:")
    for info in missing:
        print("-", info)
    print()


def function_menu_choice(input_user_choice_menu):
    choice = str(input_user_choice_menu).strip().upper()
    
    if choice == "1":
        try:
            with open("game_introduction.txt", "r", encoding="utf-8") as file:
                print(file.read())
        except FileNotFoundError:
            print("Datei 'game_introduction.txt' nicht gefunden.")
    elif choice == "A":
        game()
    elif choice == "B":
        try:
            with open("game_instructions.txt", "r", encoding="utf-8") as file:
                print(file.read())
        except FileNotFoundError:
            print("Datei 'game_instructions.txt' nicht gefunden.")
    elif choice == "C":
        print("Spielmodi sind aktuell noch in Entwicklung (TBC).")
    elif choice == "D":
        print("Spiel wird beendet. Auf Wiedersehen!")
        exit()


def game():
    difficulties = get_difficulties()
    country = random.choice(countries)
    
    infobox_data.clear()
    infobox_data.update(fetch_infobox_data(country))

    print_missing_info(infobox_data, info_difficulty)

    score = play_game(difficulties, country)

    if score > 0:
        print(f"\nWin! Score: {score}\n")
    else:
        print(f"\nGame over! Das gesuchte Land war: {country}\n")


def main():
    while True:
        print("""
--- MENÜ ---
1) Einführung zum Spiel
A. Neues Spiel
B. Spielregeln
C. Spielmodi (TBC)
D. Spiel beenden
        """)
        
        user_choice = input("Deine Wahl: ")
        function_menu_choice(user_choice)


if __name__ == '__main__':
    main()