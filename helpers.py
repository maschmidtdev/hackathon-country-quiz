import random
from config import info_difficulties, difficulty_counts
from infobox import fetch_infobox_data
from text_formatting import *

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
    return f"{BOLD}{info}{RESET}: {infobox_data[info]}"
  else:
    return get_random_info(difficulty, infobox_data)


def get_country_from_user() -> str:
  guess = input(f"{BRIGHT_WHITE}Auf welches Land tippst du?: {RESET}")

  if not guess:
    print(f"{BRIGHT_YELLOW+BOLD}Eingabe ungültig, erneute Eingabe:{RESET}")
    return get_country_from_user()

  return guess


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

    print(f"{BOLD}Missing infos{RESET}")
    for info in missing:
        print("-", info)
    print("\n")


def main():
    #print_missing_info()
    pass

if __name__ == '__main__':
    main()
