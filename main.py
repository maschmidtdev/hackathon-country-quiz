
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

    
if __name__ == '__main__':
    game()


