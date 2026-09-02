
import random
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

def high_score_screen(total_score):
    input_name_gamer = input("Bitte geben Sie Ihren Namen ein:")
    high_score_count_file(input_name_gamer, total_score)
    print(f"HIGH SCORE: {input_name_gamer} - {total_score} Punkte")

def high_score_count_file(name, score):
    with open("highscore.txt", "a", encoding="utf-8") as file:
        file.write(f"{name};{score}\n")

def function_menu_choice(input_user_choice_menu, total_score):
    if input_user_choice_menu == 1:
        with open("game_instructions.txt", "r", encoding="utf-8") as file:
            text_output = file.read()
        print(text_output)

    elif input_user_choice_menu == 2:
        score = game()
        total_score += score

    elif input_user_choice_menu == 3:
        high_score_screen(total_score)

    elif input_user_choice_menu == 4:
        print("Das Spiel wird beendet.")

    return total_score

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
    total_score = 0

    while True:
        print ("Bitte geben Sie eine Zahl für den gewünschten Menüpunkt ein:")

        print("""
        1) Spielregeln
        2) Spielbeginn
        3) High score
        4) Spiel beenden
        """)

        try:
            enter_number_menu = int(input("Ihre Auswahl: "))

            if enter_number_menu < 1 or enter_number_menu > 4:
                print("Ungültige Eingabe. Bitte geben Sie eine Zahl von 1 bis 4 ein.")
                continue

            total_score = function_menu_choice(enter_number_menu, total_score)

            if enter_number_menu == 4:
                break

        except ValueError:
            print("Ungültige Eingabe. Bitte geben Sie eine Zahl von 1 bis 4 ein.")


if __name__ == '__main__':
    main()


