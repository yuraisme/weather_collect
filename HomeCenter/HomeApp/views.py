import glob
from re import L
from django.shortcuts import render
from HomeApp.models import InsideTemp, OutsideTemp
from .services.openweather.weather_api_service import  Weather, get_weather
from .services.openweather.coordinates import  get_coordinates
from .services.openweather.exceptions import  ApiWeatherException
from django.utils.timezone import localtime

from .services.tasks import cron_task, put_weather_to_bd

# Create your views here.
def home(request):
    # data = put_weather_to_bd()
    weather =db_get_outside_temp()
    home_temp = db_get_inside_temp()
    # print(type(weather))
    utc_time = weather.timestamp
    local_time = localtime(utc_time)
    data = {'TEMP':f"{weather.temperature} °С",
            'Влажность':f"{int(weather.humidity)} %",
            'Погода':weather.weather,
            'Последний раз обновляли':local_time.strftime('%d-%m-%y %H:%M')
    }
    weather_icons = {'Дожжь':'rain',
                     'Снег':'snow',
                     'Ясно':'sun',
                     'Облачно':'clody',
                     'Туман':'fog',
                     'Гроза':'bolt',
                     }
    return render(request, "home.html", {'data_outside':data, 
                                         'type_weather':weather_icons.get(data['Погода']),
                                        'data_inside': home_temp,
                                         })

def db_get_inside_temp():
    all_inside_temps = InsideTemp.objects.latest('timestamp')
    if all_inside_temps:
        utc_time = all_inside_temps.timestamp
        local_time = localtime(utc_time)
        result = {'Температура в квартире':f"{all_inside_temps.temperature} °С",
            'Влажность':f"{all_inside_temps.humidity} %",
            'Заряд':f"{int(all_inside_temps.battery_level)} %",
            'Последний раз обновляли':local_time.strftime('%d-%m-%y %H:%M')
    }
    return result if result else {}

def db_get_outside_temp()->OutsideTemp:
    all_outside_temps = OutsideTemp.objects.latest('timestamp')
    return all_outside_temps