import json

from urllib import request


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
