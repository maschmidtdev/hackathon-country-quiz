
import random
from helpers import get_random_info, get_countries, get_country_from_user, get_difficulties, get_infobox_data, get_coordinates, get_distance


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
            distance = get_distance(get_coordinates(country), get_coordinates(guess))
            print(f"Die Hauptstadt deines Tipps liegt ca. {int(distance)} km von der Haupstadt des gesuchten Landes entfernt.")

    return score

def function_menu_choice(input_user_choice_menu):
    if input_user_choice_menu == 1:
        with open("game_instructions.txt", "r", encoding="utf-8") as file:
            text_output = file.read()
        print(text_output)

    elif input_user_choice_menu == 2:
        game()
        # Aufruf Funktion game() für Start des Spiels

    elif input_user_choice_menu == 3:
        pass
        # Spielmodi (TBC)

    elif input_user_choice_menu == 4:
        pass
        # print("Das Spiel wird beendet.")

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
1) Spielregeln
2) Spielbeginn
3) Spielmodi (TBC)
4) Spiel beenden
""")
# Punkt 2) C. mögliche Menü - Ergänzung:
    # Woher kommst du?
    # Möchtest du das Spiel nur innerhalb eines Kontinentes spielen?
    # Highscore Liste

    while True:
        try:
            enter_number_menu = int(input(
                "Bitte geben Sie eine Zahl für den gewünschten Menüpunkt ein: "
                ))

            if enter_number_menu < 1 or enter_number_menu > 4:
                print("Ungültige Eingabe. Bitte geben Sie eine Zahl von 1 bis 4 ein.")
                continue

            function_menu_choice(enter_number_menu)

            if enter_number_menu == 4:
                break

        except ValueError:
            print("Ungültige Eingabe. Bitte geben Sie eine Zahl von 1 bis 4 ein.")


if __name__ == '__main__':
    main()


