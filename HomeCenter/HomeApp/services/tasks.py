import logging
import datetime

logging.basicConfig(
    filename="/mnt/d/PROJECTS/PYTHON/DJango/home-temp/scheduled_task.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def put_weather_to_bd():
    logging.info(f"+===!!+++++++ ")
    result = {'TEMP':datetime.datetime.now().minute,'HUMADITY':datetime.datetime.now().second}
    
    print(result)
    return result




def put_home_temp_to_bd():
    pass