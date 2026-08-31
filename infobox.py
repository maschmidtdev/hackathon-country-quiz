import requests
from bs4 import BeautifulSoup

def fetch_infobox_data(url):
    headers = {"User-Agent": "QuizApp/1.0 (contact@example.com)"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[FEHLER] Anfrage fehlgeschlagen: {e}")
        return {}

    soup = BeautifulSoup(response.text, "html.parser")
    
    # In DE-Wikipedia heißen die Infobox-Tabellen oft 'infobox', 'top wage' oder 'sidebar'
    infobox = soup.find("table", class_=lambda c: c and any(k in c for k in ["infobox", "vcard", "top wage"]))
    
    if not infobox:
        print("[INFO] Keine Infobox auf der Seite gefunden.")
        return {}

    data = {}
    print(f"\n--- STARTE EXTRACT VON: {url} ---")
    
    for row in infobox.find_all("tr"):
        cells = row.find_all(["th", "td"])
        
        # Wir brauchen mindestens 2 Spalten in der Zeile
        if len(cells) >= 2:
            key = cells[0].get_text(strip=True)
            value = cells[1].get_text(" ", strip=True)
            
            # Bereinigen: Doppelpunkte am Ende von Schlüsseln entfernen
            key = key.rstrip(":")
            
            if key and value and key != value:
                data[key] = value
                print(f"✓ {key}: {value}")

    print(f"--- FERTIG! {len(data)} Einträge extrahiert. ---\n")
    return data

# Test-Aufruf
url = "https://de.wikipedia.org/wiki/Berlin"
ergebnis = fetch_infobox_data(url)