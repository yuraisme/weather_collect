from django.db import models

# Create your models here.
class InsideTemp(models.Model):
    timestamp = models.DateTimeField(primary_key=True, auto_now_add=True)  # Первичный ключ
    temperature = models.FloatField()  # Температура
    humidity = models.FloatField()     # Влажность
    battery_level = models.FloatField()  # Заряд батареи

    def __str__(self):
        return f"{self.timestamp} - {self.temperature}°C, {self.humidity}%"


class OutsideTemp(models.Model):
    timestamp = models.DateTimeField(primary_key=True, auto_now_add=True)  # Первичный ключ
    temperature = models.FloatField()  # Температура
    humidity = models.FloatField()     # Влажность
    weather = models.CharField(max_length=100)  # Погода (например, "Sunny", "Cloudy")

    def __str__(self):
        return f"{self.timestamp} - {self.temperature}°C, {self.weather}"