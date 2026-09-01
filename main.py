import io
import json
import random
import time
import urllib.parse
import urllib.request
import pygame
from helpers import (
    get_countries,
    get_country_from_user,
    get_difficulties,
    get_infobox_data,
    get_random_info,
)
from text_formatting import *

# Pygame Mixer für die Audiowiedergabe initialisieren
pygame.mixer.init()


def play_hymn(country: str):
  print(f"🔍 Suche Hymne für {country}...")

  search_query = f"Nationalhymne {country}"
  search_url = f"https://de.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(search_query)}&srnamespace=6&format=json"

  req = urllib.request.Request(search_url, headers={"User-Agent": "Mozilla/5.0"})

  try:
    data = json.loads(urllib.request.urlopen(req).read())
    results = data.get("query", {}).get("search", [])

    file_title = next(
        (
            item["title"]
            for item in results
            if item["title"].lower().endswith((".ogg", ".oga", ".mp3"))
        ),
        None,
    )

    if not file_title:
      print("❌ Keine Audiodatei auf Wikipedia gefunden.")
      return

    info_url = f"https://de.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(file_title)}&prop=imageinfo&iiprop=url&format=json"
    info_req = urllib.request.Request(
        info_url, headers={"User-Agent": "Mozilla/5.0"}
    )
    info_data = json.loads(urllib.request.urlopen(info_req).read())

    pages = info_data.get("query", {}).get("pages", {})
    audio_url = next(
        (
            page["imageinfo"][0]["url"]
            for page in pages.values()
            if "imageinfo" in page
        ),
        None,
    )

    if not audio_url:
      print("❌ Konnte Download-URL nicht abrufen.")
      return

    audio_url = audio_url.split("?")[0]
    if audio_url.startswith("//"):
      audio_url = "https:" + audio_url

    print("📥 Lade Audio...")
    audio_bytes = urllib.request.urlopen(
        urllib.request.Request(audio_url, headers={"User-Agent": "Mozilla/5.0"})
    ).read()

    ext = (
        "ogg" if audio_url.lower().endswith((".ogg", ".oga")) else "mp3"
    )
    pygame.mixer.music.load(io.BytesIO(audio_bytes), namehint=ext)
    pygame.mixer.music.play()

    print("🎵 Wiedergabe läuft (5 Sekunden)...")
    time.sleep(5)
    pygame.mixer.music.stop()
    print("✅ Fertig!")

  except Exception as e:
    print(f"❌ Fehler bei der Audiowiedergabe: {e}")


def play_game(difficulties, country, infobox_data) -> int:
  score = len(difficulties)

  for difficulty in difficulties:
    random_info = get_random_info(difficulty, infobox_data)

    if not random_info:
      score -= 1
      continue

    print(random_info)

    # Prüfen, ob der aktuelle Hinweis/Schwierigkeitsgrad die Hymne betrifft
    if (
        "hymne" in str(difficulty).lower()
        or "hymne" in str(random_info).lower()
    ):
      play_hymn(country)

    guess = get_country_from_user()

    if country.lower() == guess.lower():
      return score
    else:
      print(f"{BRIGHT_CYAN}{guess}{BRIGHT_MAGENTA} war leider falsch!\n{RESET}")
      score -= 1

  return score


def function_menu_choice(input_user_choice_menu):
  if input_user_choice_menu == 1:
    with open("game_instructions.txt", "r", encoding="utf-8") as file:
      text_output = file.read()
    print(text_output)

  elif input_user_choice_menu == 2:
    game()

  elif input_user_choice_menu == 3:
    # Spielmodi (TBC)
    print(
        f"{BRIGHT_YELLOW}Spielmodi sind noch in Entwicklung (TBC).{RESET}"
    )

  elif input_user_choice_menu == 4:
    print("Das Spiel wird beendet.")


def game():
  difficulties = get_difficulties()
  country = random.choice(get_countries())
  infobox_data = get_infobox_data(country)

  score = play_game(difficulties, country, infobox_data)

  if score > 0:
    print(
        f"{BOLD+BRIGHT_GREEN}Du hast gewonnen!{RESET}{BRIGHT_WHITE} Dein Score:"
        f" {BRIGHT_CYAN}{score}{RESET}"
    )
  else:
    print(
        f"{BOLD+BRIGHT_RED}Game over!{RESET}{BRIGHT_WHITE} Das gesuchte Land"
        f" war: {BRIGHT_CYAN}{country}{RESET}"
    )


def main():
  while True:
    print("Bitte geben Sie eine Zahl für den gewünschten Menüpunkt ein:")

    print("""
        1) Spielregeln
        2) Spielbeginn
        3) Spielmodi (TBC)
        4) Spiel beenden
        """)

    try:
      enter_number_menu = int(input("Ihre Auswahl: "))

      if enter_number_menu < 1 or enter_number_menu > 4:
        print(
            f"{BRIGHT_YELLOW+BOLD}Ungültige Eingabe. Bitte geben Sie eine Zahl"
            f" von 1 bis 4 ein.{RESET}"
        )
        continue

      function_menu_choice(enter_number_menu)

      if enter_number_menu == 4:
        break

    except ValueError:
      print(
          f"{BRIGHT_YELLOW+BOLD}Ungültige Eingabe. Bitte geben Sie eine Zahl von"
          f" 1 bis 4 ein.{RESET}"
      )


if __name__ == "__main__":
  main()