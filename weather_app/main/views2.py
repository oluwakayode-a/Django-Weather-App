"""
1. Create Model for City
2. Store the images in the model instance for each possible weather situation
3. 
"""
from django.shortcuts import render
from apixu.client import ApixuClient
from datetime import datetime
import calendar
import collections
from .forms import CityForm
from .models import City

api_key = '88d15fc3eb7d4a92b6b62345191408'
client = ApixuClient(api_key=api_key, lang="es")
# Create your views here.


def format_date(date):
    _date = date.replace('-', ' ')
    _day = datetime.strptime(_date, '%Y %m %d').weekday()

    week_day = calendar.day_name[_day]
    formatted_date = f"{week_day}, {date}"

    return formatted_date


def index(request):
    # url = 'http://api.openweathermap.org/data/2.5/forecast?q={},{}&units=metric&APPID=7cd7233b4ca74c1e1bf4fbfd5889282f'
    forecast = client.forecast(q='london', days=6)

    # s_day = str(forecast['forecast']['forecastday'][0]['date'])
    weather_forecast = collections.OrderedDict()
    for day in forecast['forecast']['forecastday']:
        weather_forecast[format_date(str(day['date']))] = [
            day['day']['maxtemp_c'], # 0
            day['day']['condition']['icon'] # 2
        ]

    print(weather_forecast)
    print(list(weather_forecast.items())[0])

    context = {'weather_forecast': weather_forecast,
               'temp': forecast['current']['temp_c'],
               'wind_dir': forecast['current']['wind_dir'],
               'wind_speed': forecast['current']['wind_kph'],
               'humidity': forecast['current']['humidity'],
               'date': list(weather_forecast.items())[0][0],
               'form' : city_form}

    return render(request, 'main/index.html', context)

def get_city(request):
    form = CityForm(request.POST)

    if form.is_valid():
        city = form.cleaned_data['city']
        new_city = City.objects.create(name=city)
