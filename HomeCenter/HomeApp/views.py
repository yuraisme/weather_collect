import glob
from re import L
from django.shortcuts import render
from HomeApp.models import InsideTemp, OutsideTemp

from .services.tasks import put_weather_to_bd

# Create your views here.
def home(request):
    data = put_weather_to_bd()
    return render(request, "home.html", {'data':put_weather_to_bd})


def db_add_inside_temp(data:dict):
    InsideTemp.objects.create(
    temperature=22.5,
    humidity=45.0,
    battery_level=85.0
)
def db_add_outside_temp(data:dict):
    OutsideTemp.objects.create(
        temperature=15.3,
        humidity=55.0,
        weather="Sunny"
    )

def db_get_inside_temp():
    all_inside_temps = InsideTemp.objects.latest('timestamp')
    return all_inside_temps if all_inside_temps else {}

def db_get_outside_temp():
    all_outside_temps = OutsideTemp.objects.latest('timestamp')
    return all_outside_temps if all_outside_temps else {}