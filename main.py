import os,requests,json
from langchain_groq import ChatGroq
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import SystemMessage,HumanMessage,AIMessage,ToolMessage
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"
GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
groq_client=ChatGroq(model='openai/gpt-oss-120b')
nvidia_client=ChatNVIDIA(model="nvidia/nemotron-3.5-lightning-30b-a3b")
groq=init_chat_model(model='qwen/qwen3.8-27b',model_provider='groq')

@tool
def get_current_date_time()->str:
    """Return Current Date and Time in ISO format"""
    return datetime.today().isoformat()

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

@tool
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

tools = {
    'get_current_date_time': get_current_date_time,
    'get_current_weather': get_current_weather
}

groq_llm=groq_client.bind_tools([get_current_date_time,get_current_weather])

def main():
    history=[]
    while True:
        user=input("Ask a Question : ")
        if not user or user.strip()=="bye":
            print("Chat Ended")
            break
        history.append(HumanMessage(content=user))
        response=groq_llm.invoke(history)
        history.append(response)
        while response.tool_calls:
            for tool_call in response.tool_calls:
                tool_response=tools[tool_call['name']].invoke(tool_call['args'])
                history.append(ToolMessage(content=tool_response,tool_call_id=tool_call['id']))
            response = groq_llm.invoke(history)
            history.append(response)
        print("AI :",response.content)
        
if __name__=="__main__":
    main()