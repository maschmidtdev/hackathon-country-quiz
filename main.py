import random

import requests
from bs4 import BeautifulSoup
from infobox import fetch_infobox_data


countries = ["Deutschland", "Frankreich", "Spanien", "Italien", "Namibia"]

info_difficulty = {
    "schwer": ["Wahlsprache","Amtssprache", "Hauptstadt"],
    "mittel": ["Staatsoberhaupt","Staatsreligion", "Fläche"],
    "leicht": ["Zeitzone","Telefonvorwahl", "Kfz-Kennzeichen"]
}


infobox_data = {}


difficulty_counts = {
    "schwer": 2,
    "mittel": 3,
    "leicht": 2
}

"""
def get_info_box(country):
    url = f"https://de.wikipedia.org/wiki/{country}"
    response = requests.get(url, headers={"User-Agent": "Quiz"})
    soup = BeautifulSoup(response.text, "html.parser")

    infobox = soup.find("table", class_="infobox")

    for row in infobox.find_all("tr"):
        text = row.get_text(separator=": ", strip=True)
"""


def get_random_info(difficulty) -> str:
    if len(info_difficulty[difficulty]) == 0:
        return ""

    info = random.choice(info_difficulty[difficulty])
    info_difficulty[difficulty].remove(info)

    if info in infobox_data:
        return f"{info}: {infobox_data[info]}"
    else:
        return get_random_info(difficulty)


def get_country_from_user() -> str:
    guess = input("Auf welches Land tippst du?: ")

    if not guess:
        print("Eingabe ungültig, erneute Eingabe:")
        return get_country_from_user()

    return guess


def play_game(difficulties, country) -> int:
    score = len(difficulties)

    for difficulty in difficulties:
        random_info = (get_random_info(difficulty))

        if not random_info:
            score -= 1
            continue

        print(random_info)
        guess = get_country_from_user()

        if country.lower() == guess.lower():
            return score
        else:
            score -= 1

    return score


def get_difficulties() -> list:
    difficulties = []
    for key, value in difficulty_counts.items():
        for i in range(value):
            difficulties.append(key)
    return difficulties


def game():
    # Menü anzeigen (siehe whiteboard/excalidraw) - Annika
    # Spielablauf/Spiellogik
    #   - interne Länder auswahl liste (kontinent auswhal später)
    #   - infobox daten fetchen - funktion dafür -> Thomas
    #   - internes dict für schwierigkeiten + infos (schwierigkeit 1, 2 und 3)
    #   - aus aktueller schwierigkeit random info auswählen + display
    #   - user input Land
    #       - Erfolg = gratulieren, punkte display, -> Menü
    #       - Falsch geraten, evtl. schwierigkeit anpassen, nächster Hinweis
    #       - nach X versuchen spiel verloren, menü ?

    # TODO: make function
    difficulties = get_difficulties()
    country = random.choice(countries)
    infobox_data.update(fetch_infobox_data(country))

    # Loop
    score = play_game(difficulties, country)

    if score > 0:
        print("Win! Score:", score)
    else:
        print("Game over! Das gesuchte Land war:", country)


if __name__ == "__main__":
    game()