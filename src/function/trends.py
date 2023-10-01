import tweepy

from src.config.config import settings


def get_trends(city, country) -> tuple:
    try:
        api_key = settings.trends_api_key
        api_secret_key = settings.api_secret_key
        auth = tweepy.AppAuthHandler(api_key, api_secret_key)
        geo = tweepy.API(auth).available_trends()
        trends = ""
        if woeid := [location["woeid"] for location in geo if location["name"] == city]:
            trends = tweepy.API(auth).get_place_trends(woeid[0])[0]["trends"]
        if trends:
            return trends, city
        else:
            woeid = [
                location["woeid"] for location in geo if location["name"] == country
            ]
            return tweepy.API(auth).get_place_trends(woeid[0])[0]["trends"], country
    except Exception as e:
        print(e)
