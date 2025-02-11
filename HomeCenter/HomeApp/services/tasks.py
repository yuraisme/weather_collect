import logging
import datetime
from re import A
from openweather.weather_api_service import  Weather, get_weather
from openweather.coordinates import  get_coordinates
from openweather.exceptions import  ApiWeatherException
from tuya.tuya_cloud import get_temp
from HomeApp.models import InsideTemp, OutsideTemp
from django.utils.timezone import localtime


logging.basicConfig(
    # filename="scheduled_task.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

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
    #now Tuya home temp
    tuya_data = get_temp()
    if tuya_data:
        db_add_inside_temp(tuya_data)
    else:
        print("Some fail coming")
        logging.info("error Tuya")
        
def db_add_inside_temp(data):
    InsideTemp.objects.create(
        temperature=data.temperature,
        humidity=data.humidity,
        battery_level = data.battery,
 
)


def db_add_outside_temp(data:Weather):
    """requested data put to DB"""
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
if __name__ == "__main__":
    cron_task()