import random
from text_formatting import *
from helpers import get_random_info, get_countries, get_country_from_user, get_difficulties, get_infobox_data, get_coordinates, get_distance


def play_game(difficulties, country, infobox_data) -> int:
    score = len(difficulties)

    for difficulty in difficulties:
        random_info = (get_random_info(difficulty, infobox_data, country))

        if not random_info:
            score -= 1
            continue

        print(f"{BRIGHT_WHITE} - - - {len(difficulties) - score +1}. Hinweis: ", end="")

        print(random_info)
        guess = get_country_from_user()

        if country.lower() == guess.lower():
            return score
        else:
            print(f"{BRIGHT_CYAN}{guess.capitalize()}{BRIGHT_MAGENTA} war leider falsch!{RESET}")
            score -= 1

            coordinates_country_to_guess = get_coordinates(country)
            coordinates_user_guess = get_coordinates(guess)
            if coordinates_country_to_guess != None and coordinates_user_guess != None:
                distance = get_distance(coordinates_country_to_guess, coordinates_user_guess)
                print(f"{BRIGHT_WHITE}Die Hauptstadt deines Tipps liegt ca. {BRIGHT_CYAN}{int(distance)}{BRIGHT_WHITE} km von der Haupstadt des gesuchten Landes entfernt.{RESET}\n")

    return score

def function_menu_choice(input_user_choice_menu):
    if input_user_choice_menu == 1:
        with open("game_instructions.txt", "r", encoding="utf-8") as file:
            text_output = file.read()
        print(text_output)

    elif input_user_choice_menu == 2:
        game()

    elif input_user_choice_menu == 3:
        pass
        # Spielmodi (TBC)

    elif input_user_choice_menu == 4:
        print("Das Spiel wird beendet.")

def game():
    difficulties = get_difficulties()
    country = str(random.choice(get_countries()))
    country = "frankreich"
    infobox_data = get_infobox_data(country)

    score = play_game(difficulties, country, infobox_data)

    if score > 0:
        print(f"{BOLD+BRIGHT_GREEN}Du hast gewonnen!{RESET}{BRIGHT_WHITE} Dein Score: {BRIGHT_CYAN}{score}{RESET}\n")
    else:
        print(f"{BOLD+BRIGHT_RED}Game over!{RESET}{BRIGHT_WHITE} Das gesuchte Land war: {BRIGHT_CYAN}{country.capitalize()}{RESET}\n")


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


