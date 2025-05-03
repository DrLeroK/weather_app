from django.urls import include, path
from . import views


app_name = 'app_weather'

urlpatterns = [
    path('', views.WeatherView.as_view(), name='app_weather'),
    
]