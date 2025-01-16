import glob
from re import L
from django.shortcuts import render
from HomeApp.models import InsideTemp, OutsideTemp
from .services.openweather.weather_api_service import  Weather, get_weather
from .services.openweather.coordinates import  get_coordinates
from .services.openweather.exceptions import  ApiWeatherException
from django.utils.timezone import localtime

from .services.tasks import put_weather_to_bd

# Create your views here.
def home(request):
    # data = put_weather_to_bd()
    weather =db_get_outside_temp()
    # print(type(weather))
    utc_time = weather.timestamp
    local_time = localtime(utc_time)
    data = {'TEMP':f"{weather.temperature} °С",
            'Влажность':f"{weather.humidity} %",
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
    return render(request, "home.html", {'data':data, 'type_weather':weather_icons.get(data['Погода'])})

def db_get_inside_temp():
    all_inside_temps = InsideTemp.objects.latest('timestamp')
    return all_inside_temps if all_inside_temps else {}

def db_get_outside_temp()->OutsideTemp:
    all_outside_temps = OutsideTemp.objects.latest('timestamp')
    return all_outside_temps