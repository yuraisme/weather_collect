from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Главная страница
    path('chart/', views.temperature_chart, name='temperature_chart'),
]