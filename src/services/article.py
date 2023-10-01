import datetime

from src.function.article import get_article


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
