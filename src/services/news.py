from src.function.news import get_news


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
