def function_menu_choice(input_user_choice_menu):
    if input_user_choice_menu == 1:
        with open("game_instructions.txt", "r", encoding="utf-8") as file:
            text_output = file.read()
        print(text_output)

    elif input_user_choice_menu == 2:
        pass
        # Aufruf Funktion game() für Start des Spiels

    elif input_user_choice_menu == 3:
        pass
        # Spielmodi (TBC)

    elif input_user_choice_menu == 4:
        pass
        # print("Das Spiel wird beendet.")


def main():
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
    # Einführungstext anzeigen
    with open("game_introduction.txt", "r", encoding="utf-8") as file:
        text = file.read()
    print(text)

    # Menü anzeigen
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


