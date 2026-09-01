import random
from config import info_difficulties, difficulty_counts
from infobox import fetch_infobox_data
from geopy.distance import geodesic
from geopy.geocoders import Nominatim


def get_infobox_data(country) -> dict:
  return fetch_infobox_data(country)


def get_info_difficulties() -> list:
  return info_difficulties


def get_countries() -> list:
  countries = []
  with open("countries.txt", "r", encoding="utf-8") as country_file:
    for country in country_file.readlines():
      countries.append(country.strip())

  return countries


def get_random_info(difficulty, infobox_data) -> str:
  if len(info_difficulties[difficulty]) == 0:
    return ""

  info = random.choice(info_difficulties[difficulty])
  info_difficulties[difficulty].remove(info)

  if info in infobox_data:
    return f"{info}: {infobox_data[info]}"
  else:
    return get_random_info(difficulty, infobox_data)


def get_country_from_user() -> str:
  guess = input("Auf welches Land tippst du?: ")

  if not guess:
    print("Eingabe ungültig, erneute Eingabe:")
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


def get_difficulties() -> list:
    difficulties = []
    for key, value in difficulty_counts.items():
        for i in range(value):
            difficulties.append(key)
    return difficulties


def print_missing_info(info_data, info_difficulty):
    missing = list(info_data.keys())
    for info in info_data:
        for key ,infolist in info_difficulty.items():
            if info in infolist:
                missing.remove(info)
                break

    print("Missing infos")
    for info in missing:
        print("-", info)


def main():
    #print_missing_info()
    pass

if __name__ == '__main__':
    main()
