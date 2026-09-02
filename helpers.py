import random
from config import info_difficulties, difficulty_counts
from infobox import fetch_infobox_data
from text_formatting import *
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from audio import play_hymn



def special_capitalize(country) -> str:
  words = country.split()
  new_words = []
  for word in words:
    if word not in ["und"]:
      new_words.append(word.capitalize())
    else:
      new_words.append(word)

  return " ".join(new_words)

def get_infobox_data(country) -> dict:
  return fetch_infobox_data(country)


def get_info_difficulties() -> list:
  return info_difficulties


def get_countries() -> list:
  countries = []
  with open("countries.txt", "r", encoding="utf-8") as country_file:
    for country in country_file.readlines():
      countries.append(country.strip().lower())

  return countries


def get_random_info(difficulty, infobox_data, country) -> str:
  if len(info_difficulties[difficulty]) == 0:
    return ""

  info = random.choice(info_difficulties[difficulty])
  info_difficulties[difficulty].remove(info)

  if info in infobox_data:
    # Flexibler Check auf "Hymne" (deckt auch unsichtbare Trennzeichen ab)
    if "hymne" in info.lower():
      play_hymn(country, infobox_data)
      return f"{BOLD+BRIGHT_GREEN}{info}{RESET} - - -\n"
    else:
      return f"{BOLD+BRIGHT_GREEN}{info}{RESET} - - -\n\t {BRIGHT_GREEN}-> {infobox_data[info]}{RESET}\n"

  else:
    return get_random_info(difficulty, infobox_data, country)


def get_country_from_user() -> str:
  guess = input(f"{BRIGHT_WHITE}Auf welches Land tippst du?: {RESET}")

  if guess.lower() not in get_countries():
    print(f"{BRIGHT_YELLOW+BOLD}Kein gültiges Land, erneute Eingabe::{RESET}")
    return get_country_from_user()

  return guess


def get_distance(country_to_find, guess_user):
    # Berechnet die Distanz direkt in Kilometern
    return geodesic(country_to_find, guess_user).km


def get_coordinates(country):
    # User-Agent ist Pflicht - sagt dem Server, wer die Anfrage schickt
    geolocator = Nominatim(user_agent="verlaender_dich_nicht")
    location = geolocator.geocode(country)
    if location:
        koordinaten = (location.latitude, location.longitude)
        return koordinaten
    else:
        return None


def get_difficulties() -> list:
    difficulties = []
    for key, value in difficulty_counts.items():
        for i in range(value):
            difficulties.append(key)
    return difficulties


def print_missing_info():
    missing = []
    for country in get_countries():
      country_infos = fetch_infobox_data(country)

      for info, value in country_infos.items():

        found = False
        for info_list in info_difficulties.values():
          if info in info_list:
            found = True
            break

        if not found:
          missing.append({"info key": info, "info value": value})

    print("MISSING")
    for item in missing:
      print(item)


def main():
    #print_missing_info()
    print(special_capitalize("bosnien und herzegowina"))


if __name__ == '__main__':
    main()