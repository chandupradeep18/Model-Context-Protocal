from mcp.server.fastmcp import FastMCP
from pydantic import Field
from typing import List
import requests
from datetime import datetime
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"
GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
mcp=FastMCP("Standard Input Output MCP Server")


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

if __name__ == "__main__":
    mcp.run(transport="stdio")