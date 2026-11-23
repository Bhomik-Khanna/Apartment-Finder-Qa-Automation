

import os
import requests
from dotenv import load_dotenv

load_dotenv()

ORS_API_KEY = os.environ.get("ORS_API_KEY")
GEOCODE_URL = "https://api.openrouteservice.org/geocode/search"
DIRECTIONS_URL = "https://api.openrouteservice.org/v2/directions/driving-car"


def _geocode(address):
    """
    Turn a text address into [longitude, latitude].
    """
    headers = {
        "Accept": "application/json, application/geo+json",
        "Authorization": ORS_API_KEY,
    }
    params = {"text": address, "size": 1}

    response = requests.get(GEOCODE_URL, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()

    features = data.get("features")
    if not features:
        raise ValueError(f"Could not find coordinates for address: {address}")

    # GeoJSON format gives coordinates as [longitude, latitude]
    return features[0]["geometry"]["coordinates"]


def get_commute_minutes(origin_address, destination_address):
    """
    Returns driving time in minutes between two addresses.
    Returns None if anything goes wrong instead of crashing the app.
    """
    if not ORS_API_KEY:
        print("Warning: ORS_API_KEY not set. Check your .env file.")
        return None

    try:
        origin_coords = _geocode(origin_address)
        dest_coords = _geocode(destination_address)

        headers = {
            "Accept": "application/json, application/geo+json",
            "Authorization": ORS_API_KEY,
        }
        params = {
            "start": f"{origin_coords[0]},{origin_coords[1]}",
            "end": f"{dest_coords[0]},{dest_coords[1]}",
        }
        response = requests.get(DIRECTIONS_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        duration_seconds = data["features"][0]["properties"]["segments"][0]["duration"]
        return round(duration_seconds / 60, 1)

    except (requests.RequestException, KeyError, IndexError, ValueError) as error:
        print(f"Distance API error: {error}")
        return None


if __name__ == "__main__":
    college = "Faridabad Railway Station, Faridabad, Haryana"
    apartment = "Sector 45, Gurgaon, Haryana"

    college_coords = _geocode(college)
    apartment_coords = _geocode(apartment)
    print(f"{college} -> coordinates: {college_coords}")
    print(f"{apartment} -> coordinates: {apartment_coords}\n")

    minutes = get_commute_minutes(college, apartment)
    print(f"Commute time: {minutes} minutes")