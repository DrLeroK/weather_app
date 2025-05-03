import requests
from django.views.generic import FormView
from datetime import datetime
from app_weather.forms import WeatherForm
from app_weather.models import WeatherSearch
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class WeatherView(LoginRequiredMixin, FormView):
    template_name = 'app_weather/app_weather.html'
    form_class = WeatherForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        city = self.request.GET.get('city')

        if city:
            api_key = os.getenv('WEATHER_API_KEY') # Ensure you have your API key in .env file
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                context['weather_data'] = {
                    'city': city,
                    'country': data['sys']['country'],
                    'temperature': data['main']['temp'],
                    'feels_like': data['main']['feels_like'],
                    'temp_min': data['main']['temp_min'],
                    'temp_max': data['main']['temp_max'],
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'wind_speed': data['wind']['speed'],
                    'wind_direction': data['wind']['deg'],
                    'visibility': data['visibility'] / 1000,  # Convert meters to km
                    'cloudiness': data['clouds']['all'],
                    'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S'),
                    'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S'),
                    'weather_condition': data['weather'][0]['main'],
                    'description': data['weather'][0]['description'],
                    'icon': f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}.png"
                }

                # **Save searched city to the database**
                if self.request.user.is_authenticated:
                    WeatherSearch.objects.create(user=self.request.user, city=city)

            else:
                context['error'] = "City not found."

        return context
    
    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # AJAX request - return JSON
            context = self.get_context_data(**kwargs)
            if 'weather_data' in context:
                return JsonResponse({'weather_data': context['weather_data']})
            elif 'error' in context:
                return JsonResponse({'error': context['error']}, status=400)
        return super().get(request, *args, **kwargs)

