from src.function.trends import get_trends


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
