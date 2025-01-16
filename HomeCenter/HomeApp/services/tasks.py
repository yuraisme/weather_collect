import logging
import datetime
from .openweather.weather_api_service import  Weather, get_weather
from .openweather.coordinates import  get_coordinates
from .openweather.exceptions import  ApiWeatherException
from HomeApp.models import InsideTemp, OutsideTemp
from django.utils.timezone import localtime

logging.basicConfig(
    filename="/mnt/d/PROJECTS/PYTHON/DJango/home-temp/scheduled_task.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)
Celcius :float

def cron_task():
    """Put some data to DB"""
    coordinates = get_coordinates()
    logging.info("Put some data to DB")
    try:
        weather = get_weather(coordinates=coordinates)

    except ApiWeatherException:
        print("Что-то с сервисом погоды, неудача")
    if weather:
       db_add_outside_temp(weather) 

def db_add_inside_temp(data:Weather):
    InsideTemp.objects.create(
        temperature=14.3,
        humidity=54.0,
        weather="Sunny"
 
)


def db_add_outside_temp(data:Weather):
    OutsideTemp.objects.create(
    temperature=data.temperature,
    humidity=data.humidity,
    weather=data.weather_type.value
   )


def put_weather_to_bd():
    logging.info(f"+===!!+++++++ ")
    
    coordinates = get_coordinates()
    try:
        weather = get_weather(coordinates=coordinates)

    except ApiWeatherException:
        print("Что-то с сервисом погоды, неудача")
    if weather:
        result = {'TEMP':weather.temperature,
                  'HUMADITY':weather.humidity,
                  'WEATHER':weather.weather_type.value}
                  
    
    print(result)
    return result




def put_home_temp_to_bd():
    pass