from mcp.server.fastmcp import FastMCP
from pydantic import Field
from typing import List
import requests,os
from datetime import datetime
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"
GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
mcp=FastMCP("HTTP Input Output MCP Server")
from dotenv import load_dotenv
load_dotenv()

TMDB_ACCESS_TOKEN = os.getenv("TMDB_ACCESS_TOKEN")

BASE_URL = "https://api.themoviedb.org/3"


def fetch_city_location(place_name:str)->dict():
    params = {"name": place_name,'country_code':'IN',"count": 1,"language": "en","format": "json"}
    geo_response=requests.get(GEO_URL,params=params,timeout=30)
    geo_data=geo_response.json()
    results = geo_data.get("results", [])
    if results:
        return {"latitude":geo_data['results'][0]['latitude'],"longitude":geo_data['results'][0]['longitude'],"city":place_name}
    else:
        return None

def fetch_city_weather(place_location:dict())->dict():
    params = {"latitude": place_location.get('latitude'),
    "longitude": place_location.get('longitude'),
    "current": ["temperature_2m","relative_humidity_2m","apparent_temperature","precipitation","wind_speed_10m"]}
    response=requests.get(WEATHER_API_URL,params=params,timeout=30)
    response.raise_for_status()
    data = response.json()
    if data:
        city_data={}
        city_data['city']=place_location.get('city')
        city_data['latitude']=place_location.get('latitude')
        city_data['longitude']= place_location.get('longitude')
        city_data['time']=data['current']['time']
        city_data['temperature']=f"{data['current']['temperature_2m']}{data['current_units']['temperature_2m']}"
        city_data['humidity']=f"{data['current']['relative_humidity_2m']}{data['current_units']['relative_humidity_2m']}"
        city_data['apparent_temperature']=f"{data['current']['apparent_temperature']}{data['current_units']['apparent_temperature']}"
        city_data['Wind Speed']=f"{data['current']['wind_speed_10m']}{data['current_units']['wind_speed_10m']}"
        return city_data
    return None

@mcp.tool()
def get_current_weather(place_name:str):
    """Get the current weather information for a given Indian city."""
    if not place_name:
        raise ValueError('Place Name is Required')
    place_name=place_name.strip()
    response=fetch_city_location(place_name)
    if response:
        weather=fetch_city_weather(response)
        if weather:
            return weather
        return "No Weather Data Found"
    else:
        return "Invaild Place Name Not Data Found"
    
@mcp.tool()
def get_current_date_time()->str:
    """Return Current Date and Time in ISO format"""
    return datetime.today().isoformat()

@mcp.tool()
def search_tmdb(query: str,page: int = 1,language: str = "en-US",include_adult: bool = False) -> dict:
    """
    Search for movies, TV shows and people using TMDB.

    Args:
        query: Movie name, TV show name or person name.
        page: Page number for pagination.
        language: Language for the response.
        include_adult: Whether to include adult content.
    """
    if not TMDB_ACCESS_TOKEN:
        return {"error": "TMDB API token is not configured."}

    if not query.strip():
        return {"error": "Search query cannot be empty."}

    if page < 1:
        return {"error": "Page must be greater than zero."}

    url = f"{BASE_URL}/search/multi"

    headers = {
        "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}",
        "accept": "application/json"
    }

    params = {
        "query": query,
        "include_adult": include_adult,
        "language": language,
        "page": page
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        results = []

        for item in data.get("results", []):

            media_type = item.get("media_type")

            result = {
                "id": item.get("id"),
                "media_type": media_type,
                "name": item.get("title") or item.get("name"),
                "overview": item.get("overview"),
                "popularity": item.get("popularity"),
                "vote_average": item.get("vote_average"),
                "poster_path": item.get("poster_path")
            }

            if media_type == "movie":
                result["release_date"] = item.get("release_date")

            elif media_type == "tv":
                result["first_air_date"] = item.get("first_air_date")

            elif media_type == "person":
                result["known_for_department"] = item.get(
                    "known_for_department"
                )

            results.append(result)

        return {
            "query": query,
            "page": data.get("page"),
            "total_pages": data.get("total_pages"),
            "total_results": data.get("total_results"),
            "results": results
        }

    except requests.exceptions.HTTPError as e:
        return {
            "error": "TMDB API returned an HTTP error",
            "details": str(e)
        }

    except requests.exceptions.RequestException as e:
        return {
            "error": "Unable to connect to TMDB",
            "details": str(e)
        }



if __name__ == "__main__":
    mcp.run(transport="streamable-http")