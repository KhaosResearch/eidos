import requests

from eidos.logs import get_logger

logger = get_logger("eidos.functions")


def salute(who: str) -> str:
    """Salute someone.

    Args:
        who (str): The name of whom to salute. o7

    Returns:
        msg (str): The salutation message.
    """
    return f"Hello, {who}! o7"


def geocode(location: str) -> tuple[float, float]:
    """Get the coordinates of a location using OpenStreetMap. This is also known as
    geocoding.

    Args:
        location (str): The location to get the coordinates of.

    Returns:
        coordinates(tuple[float, float]): The latitude and longitude of the location.
    """

    endpoint = "https://nominatim.openstreetmap.org/search"
    params = {"q": location, "format": "json"}

    response = requests.get(endpoint, params=params)

    # If there is no error, get the coordinates
    if response.status_code == 200:
        data = response.json()
        lat, lon = float(data[0]["lat"]), float(data[0]["lon"])
    else:
        logger.info(f"Location not found: {location}")
        raise ValueError(f"Location not found: {location}")

    return (lat, lon)


def ddg_search(query: str) -> str:
    """Search DuckDuckGo for a query. For limitations in the duckduckgo API, if there
    is no abstract text, it only returns a link to the search results.
    
    Args:
        query (str): The query to search for.
        
    Returns:
        result (str): The result of the search.
    """
    endpoint = "https://duckduckgo.com/"
    params = {"q": query, "format": "json", "pretty": "0"}

    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        data = response.json()

        if data["AbstractText"]:
            return data["AbstractText"]
        else:
            return (
                f"You can read more about {query} at "
                f"{data['RelatedTopics'][0]['FirstURL']}"
            )
    else:
        logger.info(f"Search not found: {query}")
        raise ValueError(f"Search not found: {query}")
