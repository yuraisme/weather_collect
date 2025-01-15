from django.contrib import admin
from .models import InsideTemp, OutsideTemp

@admin.register(InsideTemp)
class InsideTempAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'temperature', 'humidity', 'battery_level')

@admin.register(OutsideTemp)
class OutsideTempAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'temperature', 'humidity', 'weather')

# Register your models here.
