import random
from text_formatting import *
from config import MAX_LIVES
from helpers import (
    get_random_info,
    get_countries,
    get_country_from_user,
    get_difficulties,
    get_info_difficulties,
    get_infobox_data,
    get_coordinates,
    get_distance, display_lives
)



def play_game(difficulties, country, infobox_data) -> int:
    score = len(difficulties)
    info_difficulties = get_info_difficulties()

    for difficulty in difficulties:
        random_info = get_random_info(difficulty, info_difficulties, infobox_data, country)

        if not random_info:
            score -= 1
            continue

        max_hints = len(difficulties)
        current_hint = max_hints - score + 1

        print(f"{BRIGHT_WHITE} - - - Hinweis {current_hint}/{max_hints} ({difficulty}) ", end="")

        print(random_info)
        guess = get_country_from_user()

        if country.lower() == guess.lower():
            return score
        else:
            print(f"{BRIGHT_CYAN}{guess.capitalize()}{BRIGHT_MAGENTA} war leider falsch!{RESET}")
            score -= 1
            distance = get_distance(get_coordinates(country), get_coordinates(guess))
            print(f"{BRIGHT_WHITE}Die Hauptstadt deines Tipps liegt ca. {BRIGHT_CYAN}{int(distance)}{BRIGHT_WHITE} km von der Haupstadt des gesuchten Landes entfernt.{RESET}\n")

    return score

def function_menu_choice(input_user_choice_menu):
    if input_user_choice_menu == 1:
        with open("game_instructions.txt", "r", encoding="utf-8") as file:
            text_output = file.read()
        print(text_output)

    elif input_user_choice_menu == 2:
        game(MAX_LIVES)

    elif input_user_choice_menu == 3:
        pass
        # Spielmodi (TBC)

    elif input_user_choice_menu == 4:
        print("Das Spiel wird beendet.")

def game(lives, score = 0):
    difficulties = get_difficulties()
    country = str(random.choice(get_countries()))
    infobox_data = get_infobox_data(country)

    new_score = play_game(difficulties, country, infobox_data)

    if new_score > 0:
        new_score += score
        print(f"{BOLD+BRIGHT_GREEN}Korrekt!{RESET}{BRIGHT_WHITE} Dein aktueller Score: {BRIGHT_CYAN}{new_score}{RESET}")
        display_lives(lives, MAX_LIVES)
        game(lives, new_score)

    else:
        lives -= 1
        print(f"{BOLD+BRIGHT_RED}Das wars!{RESET}{BRIGHT_WHITE} Das gesuchte Land war: {BRIGHT_CYAN}{country.capitalize()}{RESET}")
        display_lives(lives, MAX_LIVES)

        if lives > 0:
            game(lives, score)
        else:
            print(f"{BRIGHT_RED}Game Over!{RESET}{BRIGHT_WHITE} Dein Score: {BRIGHT_CYAN}{score}{RESET}\n")

        # input highscore


def main():
# Punkt 2) C. mögliche Menü - Ergänzung:
    # Woher kommst du?
    # Möchtest du das Spiel nur innerhalb eines Kontinentes spielen?
    # Highscore Liste

    while True:
        print ("Bitte geben Sie eine Zahl für den gewünschten Menüpunkt ein:")

        print("""
        1) Spielregeln
        2) Spielbeginn
        3) Spielmodi (TBC)
        4) Spiel beenden
        """)

        try:
            enter_number_menu = int(input("Ihre Auswahl: "))

            if enter_number_menu < 1 or enter_number_menu > 4:
                print(f"{BRIGHT_YELLOW+BOLD}Ungültige Eingabe. Bitte geben Sie eine Zahl von 1 bis 4 ein.{RESET}")
                continue

            function_menu_choice(enter_number_menu)

            if enter_number_menu == 4:
                break

        except ValueError:
            print(f"{BRIGHT_YELLOW+BOLD}Ungültige Eingabe. Bitte geben Sie eine Zahl von 1 bis 4 ein.{RESET}")


if __name__ == '__main__':
    main()