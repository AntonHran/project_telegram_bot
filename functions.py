import re
import csv
import json
import tweepy
import datetime
import random

from urllib import request
from bs4 import BeautifulSoup
import newsapi
import requests
from googletranslatepy import Translator


def get_api_key(name: str) -> str:
    with open("token.txt", "r") as file:
        for line in file.readlines():
            if re.match(name, line):
                api_key = line.replace(name + " = ", "").strip()
                return api_key


def scrap_quotes():
    page = "https://www.oberlo.com/blog/motivational-quotes"
    res = requests.get(page)
    soup = BeautifulSoup(res.text, "lxml")
    quotes = soup.select("li")
    q = [
        quote.text.replace("“", "")
        .replace("”", "")
        .replace("―", "-")
        .replace("—", "-")
        .replace("–", "-")
        for quote in quotes
        if quote.text.startswith("“")
    ]
    # [print(el) for el in q]
    with open("quotes.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["quote", "author"], quoting=1)
        writer.writeheader()
        for quote in q:
            try:
                qu, author = quote.rsplit("-", 1)
            except ValueError:
                pass
            writer.writerow({"quote": qu.strip(), "author": author.strip()})


def get_article():
    try:
        data = json.load(
            request.urlopen("https://en.wikipedia.org/api/rest_v1/page/random/summary")
        )
        return {
            "title": data["title"],
            "extract": data["extract"],
            "url": data["content_urls"]["desktop"]["page"],
        }
    except Exception as e:
        print(e)


def get_weather(city_name):
    city_name = city_name.replace(" ", "+")
    try:
        api_key = get_api_key("weather_api_key")
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


def get_trends(city, country) -> tuple:
    try:
        api_key = get_api_key("trends_api_key")
        api_secret_key = get_api_key("api_secret_key")
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


def get_news(categories: list, countries: list) -> list:
    api_key = get_api_key("news_api_key")
    api = newsapi.NewsApiClient(api_key)
    results = []
    for country in countries:
        for category in categories:
            results.append(
                api.get_top_headlines(
                    category=category, country=country, page_size=3, page=1
                )
            )
    print(results)
    return results


def get_books():
    pass


def form_news(cat: list, count: list) -> list:
    lst = []
    res = get_news(cat, count)
    for result in res:
        for el in result["articles"]:
            article_data = f"""Source: {el['source']['name']}
    Title: {el['title']}
    Author: {el['author']}
    Content: {el['content']}
    Date: {el['publishedAt']}
    url: {el['url']}\n"""
            lst.append(article_data)
    return lst


def translate(text: str) -> str:
    trnas = Translator()
    if len(text) < 5000:
        text = trnas.translate(text)
        return text
    else:
        text = [text[i: i + 5000] for i in range(0, len(text), 5000)]
        return "".join(text)


def form_quote(time: datetime.time) -> str:
    lst = []
    with open("quotes.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file, fieldnames=["quote", "author"], quoting=1)
        for row in reader:
            lst.append(row)
    res = random.choice(lst)
    return f"{res['quote']} | Author: {res['author']}. at time {time}"


def form_article(time: datetime.time) -> str:
    article_dict = get_article()
    text = ""
    if article_dict:
        text += "*~*~*  Daily Random Learning  *~*~*\n\n"
        text += (
            f'Time: {time}, {article_dict["title"]}\n<{article_dict["url"]}>'
            f'\n{article_dict["extract"]}'
        )
    return text


def form_weather(city_name):
    message = ""
    forecast = get_weather(city_name)
    if forecast:
        message = f"Forecast for {forecast['city']}, {forecast['country']}:\n\n"
        for period in forecast["periods"]:
            message += f"{period['timestamp'].strftime('%d %b %H:%M')}\n"
            message += f"Temperature: {period['temp']}°C\n"
            message += f"Description: {period['description']}\n\n"
    return message


def form_trends(text_from):
    city, country = text_from.split(" ")
    trends = get_trends(city=city, country=country)
    text = ""
    if trends:
        text += f"*~*~*  Top Ten Twitter Trends in {trends[1]}  *~*~*\n\n"
        for trend in trends[0][0:10]:
            text += f'- {trend["name"]}: {trend["url"]}\n\n'
        text += "\n"
    return text


def form_books():
    pass


def make_search(keyword):
    pass
