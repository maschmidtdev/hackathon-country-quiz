from geopy.distance import geodesic
from geopy.geocoders import Nominatim

def calculate_distance(country_to_find, guess_user):
    # Berechnet die Distanz direkt in Kilometern
    return geodesic(country_to_find, guess_user).km


def get_coordinates(country):
    # User-Agent ist Pflicht - sagt dem Server, wer die Anfrage schickt
    geolocator = Nominatim(user_agent="verlaender_dich_nicht")
    location = geolocator.geocode(country)
    if location:
        koordinaten = (location.latitude, location.longitude)
        return koordinaten


guess_user = input("Gib ein Land ein: ")
country = "Frankreich" # Hier ist unser gewähltes Land im Spiel

distance = calculate_distance(get_coordinates(country), get_coordinates(guess_user))
print(f"Die Hauptstadt deines Tipps liegt ca. {int(distance)} km von der Haupstadt des gesuchten Landes entfernt.")
