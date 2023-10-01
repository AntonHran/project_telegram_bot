import newsapi

from src.config.config import settings


def get_news(categories: list, countries: list) -> list:
    api_key = settings.news_api_key
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
