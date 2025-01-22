from geopy.distance import geodesic
import requests

def calculate_distance(coord1, coord2):
    """
    Calculate the straight-line distance between two coordinates in meters.
    :param coord1: Tuple (latitude, longitude)
    :param coord2: Tuple (latitude, longitude)
    :return: Distance in meters
    """
    return int(geodesic(coord1, coord2).meters)

BASE_URL = "https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/"

def fetch_venue_data(venue_slug):
    """
    Fetch static and dynamic data for a given venue.
    :param venue_slug: Venue slug identifier
    :return: Tuple (static_data, dynamic_data)
    """
    static_url = f"{BASE_URL}{venue_slug}/static"
    dynamic_url = f"{BASE_URL}{venue_slug}/dynamic"

    static_response = requests.get(static_url)
    dynamic_response = requests.get(dynamic_url)

    if static_response.status_code == 200 and dynamic_response.status_code == 200:
        return static_response.json(), dynamic_response.json()
    else:
        return None, None
