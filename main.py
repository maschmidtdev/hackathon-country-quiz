import random
import json
from helpers import get_random_info, get_countries, get_country_from_user, get_difficulties, get_infobox_data


def play_game(difficulties, country, infobox_data) -> int:
    score = len(difficulties)

    for difficulty in difficulties:
        random_info = (get_random_info(difficulty, infobox_data))

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
    difficulties = get_difficulties()
    country = random.choice(get_countries())
    infobox_data = get_infobox_data(country)

    score = play_game(difficulties, country, infobox_data)

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
