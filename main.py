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
    get_distance,
    special_capitalize,
    display_lives,
    preload_country_data
)


def play_game(difficulties, country, infobox_data, cheat) -> int:
    score = len(difficulties)
    info_difficulties = get_info_difficulties()

    for difficulty in difficulties:
        random_info = get_random_info(difficulty, info_difficulties, infobox_data, country)
        if not random_info:
            score -= 1
            continue

        max_hints = len(difficulties)
        current_hint = max_hints - score + 1

        if cheat:
            print(f"Gesuchtes Land: {CHEAT}{country}{RESET}")

        print(f"{BRIGHT_WHITE} - - - Hinweis {current_hint}/{max_hints} ({difficulty}) ", end="")
        print(random_info)
        guess = get_country_from_user()

        if country.lower() == guess.lower():
            return score
        else:
            print(f"{BRIGHT_CYAN}{special_capitalize(guess)}{BRIGHT_MAGENTA} war leider falsch!{RESET}")
            score -= 1

            try:
                coordinates_country_to_guess = get_coordinates(special_capitalize(country))
                coordinates_user_guess = get_coordinates(guess)

                if coordinates_country_to_guess != None and coordinates_user_guess != None:
                    distance = get_distance(coordinates_country_to_guess, coordinates_user_guess)
                    print(f"{BRIGHT_WHITE}Die Hauptstadt deines Tipps liegt ca. {BRIGHT_CYAN}{int(distance)}{BRIGHT_WHITE} km von der Haupstadt des gesuchten Landes entfernt.{RESET}\n")
            except:
                print("(Exception: Distanz konnte nicht abgefragt werden)\n")

    return score


def high_score_screen():
    try:
        with open("highscore.txt", "r", encoding="utf-8") as file:
            high_scores = file.readlines()

    except FileNotFoundError:
        print("Es gibt noch keine Highscores.")
        return

    high_scores.sort(
        key=lambda line:int(line.strip().split(";")[1]),
        reverse=True
    )

    for i in range(len(high_scores)):
        match i:
            case 0:
                rank_color = BRIGHT_YELLOW
            case 1:
                rank_color = BRIGHT_WHITE
            case 2:
                rank_color = BRONZE
            case _:
                rank_color = RESET

        name, score = high_scores[i].strip().split(";")
        print(f"{i+1}. {rank_color}{name} - {score}{RESET}")


def high_score_count_file(score):
    input_name_gamer = input("Bitte geben Sie Ihren Namen ein: ")

    with open("highscore.txt", "a", encoding="utf-8") as file:
        file.write(f"{input_name_gamer};{score}\n")


def function_menu_choice(input_user_choice_menu):
    if input_user_choice_menu == 1:
        with open("game_instructions.txt", "r", encoding="utf-8") as file:
            text_output = file.read()
        print(text_output)

    elif input_user_choice_menu == 2:
        game(MAX_LIVES)

    elif input_user_choice_menu == 3:
        game(MAX_LIVES, 0, True)

    elif input_user_choice_menu == 4:
        high_score_screen()

    elif input_user_choice_menu == 5:
        print("Das Spiel wird beendet.")


def game(lives, score = 0, cheat = False):
    difficulties = get_difficulties()
    country = str(random.choice(get_countries()))
    # for testing
    #country = "deutschland"

    # Pre-Fetching beim Spielstart
    preload_country_data(country)

    infobox_data = get_infobox_data(special_capitalize(country))
    new_score = play_game(difficulties, country, infobox_data, cheat)

    if new_score > 0:
        new_score += score
        print(f"{BOLD+BRIGHT_GREEN}Korrekt!{RESET}{BRIGHT_WHITE} Dein aktueller Score: {BRIGHT_CYAN}{new_score}{RESET}")
        display_lives(lives, MAX_LIVES)
        game(lives, new_score, cheat)

    else:
        lives -= 1
        print(f"{BOLD+BRIGHT_RED}Das wars!{RESET}{BRIGHT_WHITE} Das gesuchte Land war: {BRIGHT_CYAN}{special_capitalize(country)}{RESET}")
        display_lives(lives, MAX_LIVES)

        if lives > 0:
            game(lives, score, cheat)
        else:
            print(f"{BRIGHT_RED}Game Over!{RESET}{BRIGHT_WHITE} Dein Score: {BRIGHT_CYAN}{score}{RESET}\n")
            high_score_count_file(score)


def main():
    with open("game_introduction.txt", "r", encoding="utf-8") as file:
        introduction = file.read()
        print(f"{BRIGHT_GREEN}\n- - - Verländer dich nicht! - - -{BRIGHT_WHITE}" )
        print(introduction)
        print(RESET)

    while True:
        print("Bitte geben Sie eine Zahl für den gewünschten Menüpunkt ein:")

        print("""
        1) Spielregeln
        2) Spielbeginn
        3) Spielbeginn (Demo cheat mode)
        4) High score
        5) Spiel beenden
        """)

        try:
            enter_number_menu = int(input("Ihre Auswahl: "))

            if enter_number_menu < 1 or enter_number_menu > 5:
                print(f"{BRIGHT_YELLOW+BOLD}Ungültige Eingabe. Bitte geben Sie eine Zahl von 1 bis 5 ein.{RESET}")
                continue

            function_menu_choice(enter_number_menu)

            if enter_number_menu == 5:
                break

        except ValueError:
            print(f"{BRIGHT_YELLOW+BOLD}Ungültige Eingabe. Bitte geben Sie eine Zahl von 1 bis 5 ein.{RESET}")


if __name__ == '__main__':
    main()


