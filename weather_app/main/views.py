from django.shortcuts import render
from apixu.client import ApixuClient
from datetime import datetime
import calendar
import collections
from .forms import CityForm

api_key = '88d15fc3eb7d4a92b6b62345191408'
client = ApixuClient(api_key=api_key, lang="en")

def format_date(date):
    _date = date.replace('-', ' ')
    _day = datetime.strptime(_date, '%Y %m %d').weekday()

    week_day = calendar.day_name[_day]
    formatted_date = f"{week_day}"

    return formatted_date


def index(request):
    form = CityForm()

    context = {
        'form' : form
    }

    return render(request, 'main/index.html', context)

def get_weather(request):
    city = request.POST['city']
    
    # check if user has submitted a city in the form.
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = request.POST['city']

    forecast = client.forecast(q=city, days=7)

    # create ordered dictionary to allow for indexing.
    weather_forecast = collections.OrderedDict()
    
    for day in forecast['forecast']['forecastday']:
        weather_forecast[format_date(str(day['date']))] = [
            day['day']['maxtemp_c'], # 0
            day['day']['condition']['icon'] # 1
        ]
    
    # get all weather conditions excluding the current day.
    # current day will be gotten from the current dict. in the API
    weather_forecast.popitem(last=False)

    context = {'weather_forecast': weather_forecast,
               'temp': forecast['current']['temp_c'],
               'wind_dir': forecast['current']['wind_dir'],
               'wind_speed': forecast['current']['wind_kph'],
               'humidity': forecast['current']['humidity'],
               'date': datetime.now(),
               'form' : form,
               'city' : city,
               'icon' : forecast['current']['condition']['icon']
                   }

    return render(request, 'main/weather.html', context)

