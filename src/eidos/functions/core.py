import requests

from eidos.logs import get_logger

logger = get_logger()

def salute(who: str) -> str:
    """Salute someone.
    
    Args:
        who (str): The name of whom to salute. o7
    
    Returns:
        str: The salutation message.
    """
    return f"Hello, {who}! o7"


def get_coordinates_by_location(location: str) -> tuple[float, float]:
    """Get the coordinates of a location using OpenStreetMap.

    Args:
        location (str): The location to get the coordinates of.

    Returns:
        tuple[float, float]: The latitude and longitude of the location.
    """

    endpoint = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': location,
        'format': 'json'
    }

    response = requests.get(endpoint, params=params)
    data = response.json()

    if data:
        lat, lon = float(data[0]['lat']), float(data[0]['lon'])
        return lat, lon
    else:
        logger.info(f"Location not found: {location}")
        return None
