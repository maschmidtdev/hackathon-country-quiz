import random
import json
from infobox import fetch_infobox_data


with open("info_difficulties.json", "r") as info_file:
    info_difficulties = json.loads(info_file.read())
    print(info_difficulties)

infobox_data = {}

difficulty_counts = {
    "schwer": 2,
    "mittel": 3,
    "leicht": 2
}

def get_countries() -> list:
    countries = []
    with open("countries.txt", "r", encoding="utf-8") as country_file:
        for country in country_file.readlines():
            countries.append(country.strip())

    return countries


def get_random_info(difficulty) -> str:
    if len(info_difficulties[difficulty]) == 0:
        return ""

    info = random.choice(info_difficulties[difficulty])
    info_difficulties[difficulty].remove(info)

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


def print_missing_info(infobox_data, info_difficulty):
    missing = list(infobox_data.keys())
    for info in infobox_data:
        for key ,infolist in info_difficulty.items():
            if info in infolist:
                missing.remove(info)
                break

    print("Missing infos")
    for info in missing:
        print("-", info)

def function_menu_choice(input_user_choice_menu):
    if input_user_choice_menu == 1:
        with open(game_introduction.txt, "r", encoding="utf-8") as file:
            text = file.read()
        print(text)
    elif input_user_choice_menu == 2:
        if input_user_choice_menu == A:
            pass
            # Funktionsaufruf für Start des Spiels
        elif input_user_choice_menu == B:
            with open(game_instructions.txt, "r", encoding="utf-8") as file:
                text_output = file.read()
            print(text_output)
        elif input_user_choice_menu == C:
            pass
            # Spielmodi (TBC)
        elif input_user_choice_menu == C:
            pass
            # Aufruf Funktion zum Beenden des Spiels



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
    country = random.choice(get_countries())
    infobox_data.update(fetch_infobox_data(country))

    print_missing_info(infobox_data, info_difficulties)

    # Loop
    score = play_game(difficulties, country)

    if score > 0:
        print("Win! Score:", score)
    else:
        print("Game over! Das gesuchte Land war:", country)
    



def main():
    print("""
    1) Einführung zum Spiel
    2) Wähle folgende Option:
        A. Neues Spiel
        B. Spielregeln
        C. Spielmodi (TBC)
        D. Spiel beenden
    """)

    # Punkt 2) C. mögliche Ergänzung:
    # Woher kommst du?
    # Möchtest du das Spiel nur innerhalb eines Kontinentes spielen?
    # Highscore Liste

    game()
    
if __name__ == '__main__':
    main()
