import requests
from bs4 import BeautifulSoup

def fetch_infobox_data(country, verbose = False):
    url = f"https://de.wikipedia.org/wiki/{country}"

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

    # --- FLAGGEN-EXTRAKTION ---
    flag_img = infobox.find("img", alt=lambda a: a and "flagge" in a.lower())
    if not flag_img:
        # Fallback: Erstes Bild in der Infobox suchen
        flag_img = infobox.find("img")

    if flag_img and "src" in flag_img.attrs:
        src = flag_img["src"]
        if src.startswith("//"):
            src = "https:" + src
        data["Flagge"] = src
        data["Fahne"] = src

    if verbose:
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
                if verbose:
                    print(f"✓ {key}: {value}")

    if verbose:
        print(f"--- FERTIG! {len(data)} Einträge extrahiert. ---\n")

    return data


if __name__ == '__main__':
    # Test-Aufruf
    country = "Deutschland"
    ergebnis = fetch_infobox_data(country, True)
    print(ergebnis)