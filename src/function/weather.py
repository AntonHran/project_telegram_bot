import json
import datetime

from urllib import request

from src.config.config import settings


def get_weather(city_name):
    city_name = city_name.replace(" ", "+")
    try:
        api_key = settings.weather_api_key
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}"
        data = json.load(request.urlopen(url))

        forecast = {
            "city": data["city"]["name"],
            "country": data["city"]["country"],
            "periods": list(),
        }

        for period in data["list"][0:9]:
            forecast["periods"].append(
                {
                    "timestamp": datetime.datetime.fromtimestamp(period["dt"]),
                    "temp": round(period["main"]["temp"] - 273),
                    "description": period["weather"][0]["description"].title(),
                    "icon": f'http://openweathermap.org/img/wn/{period["weather"][0]["icon"]}',
                }
            )
        return forecast

    except Exception as e:
        print(e)
        return None
