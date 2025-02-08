from datetime import datetime
import glob
import json
from re import L
from zoneinfo import ZoneInfo
from django.http import HttpResponse
from django.shortcuts import render
from HomeApp.models import InsideTemp, OutsideTemp
from .services.openweather.weather_api_service import  Weather, get_weather
from .services.openweather.coordinates import  get_coordinates
from .services.openweather.exceptions import  ApiWeatherException
from django.utils.timezone import localtime
from django.core.serializers.json import DjangoJSONEncoder
from django.db import connection


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
def temperature_chart(request):
    # data_inside = InsideTemp.objects.all().order_by('timestamp')
    # data_outside = OutsideTemp.objects.all().order_by('timestamp')
       
    # res_chart_inside = [ dict(x=localtime(item.timestamp).strftime('%y-%m-%d %H:%M'), 
    #                    y=item.temperature) for item in data_inside]  
    
    #Convert lists to JSON so they can be easily used in JavaScript
    # print(json.dumps(timestamps_inside, cls=DjangoJSONEncoder))
    collected_data = get_all_data()
    inside_temperature = []
    outside_temperature = []
    inside_humadity = []
    outside_humadity = []
    timestamps = []
    for item in collected_data:
        inside_temperature.append(#{'x':item['timestamp_'][2:]+':00',
                                  item['avg_inside_temp'])

        outside_temperature.append(#{'x':item['timestamp_'][2:]+':00',
                                  item['out_temp_smooth'])
         
        inside_humadity.append({'x':item['timestamp_'][2:]+':00',
                                  'y':item['avg_inside_humidity']})

        outside_humadity.append({'x':item['timestamp_'][2:]+':00',
                                  'y':item['avg_outside_humidity']})
        # if "12" in item['timestamp_']:
        timestamps.append([item['timestamp_'][2:-3], item['timestamp_'][-3:]+':00'])

    context = {        
        'inside_temperature':json.dumps(inside_temperature, cls=DjangoJSONEncoder),
        'outside_temperature':json.dumps(outside_temperature, cls=DjangoJSONEncoder),
        'inside_humadity':json.dumps(inside_humadity, cls=DjangoJSONEncoder),
        'outside_humadity':json.dumps(outside_humadity, cls=DjangoJSONEncoder),
        'timestamps':json.dumps(timestamps, cls=DjangoJSONEncoder),
    }
    return render(request, 'charts.html', context)

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

def get_all_data():
    query = """
    SELECT 
    strftime('%Y-%m-%d %H', datetime(it.timestamp, '+3 hours')) AS timestamp_,
    AVG(ot.temperature) OVER (ORDER BY ot.timestamp ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS out_temp_smooth,
    AVG(it.temperature) AS avg_inside_temp,
    AVG(ot.temperature) AS avg_outside_temp,
    AVG(it.humidity) AS avg_inside_humidity,
    AVG(ot.humidity) AS avg_outside_humidity,
    ot.weather 
    FROM 
        HomeApp_insidetemp AS it
    JOIN 
        HomeApp_outsidetemp AS ot
    ON 
        strftime('%Y-%m-%d %H:%M', it.timestamp) = strftime('%Y-%m-%d %H:%M', ot.timestamp)
    GROUP BY 
        timestamp_;
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        # Получаем названия колонок
        columns = [col[0] for col in cursor.description]
        # Преобразуем результат в список словарей
        data = [dict(zip(columns, row)) for row in cursor.fetchall()] 
        # print(data)
    return data


