import datetime

from telegram import Update
from telegram.ext import ContextTypes

from main import data, get_chat_id
from article import form_article
from book import form_books
from quote import form_quote
from news import form_news
from trends import form_trends
from weather import form_weather
from assist_functions import translate


def get_access(chat_id):  # ???
    func = {
        "article": (
            form_article,
            data[chat_id]["article"][1] if data[chat_id]["article"] else None,
        ),
        "books": (
            form_books,
            data[chat_id]["books"][1] if data[chat_id]["books"] else None,
        ),
        "motivation": (
            form_quote,
            data[chat_id]["motivation"][1] if data[chat_id]["motivation"] else None,
        ),
        "news": (
            form_news,
            [data[chat_id]["news"]["category"], data[chat_id]["news"]["country"]]
            if data[chat_id]["news"]["category"]
            else None,
        ),
        "trends": (
            form_trends,
            data[chat_id]["trends"][0] if data[chat_id]["trends"] else None,
        ),
        "weather": (
            form_weather,
            data[chat_id]["weather"][1] if data[chat_id]["weather"] else None,
        ),
    }
    return func


async def form_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id_ = await get_chat_id(update, context)
    func = get_access(chat_id_)
    lang = context.user_data["lang"]
    for key, value in data[chat_id_].items():
        if key in func and func[key][1]:
            f = func[key][0]
            if type(func[key][1]) is datetime.time or type(func[key][1]) is str:
                arg = func[key][1]
                mes = f(arg)
            elif type(func[key][1]) is list:
                mes = f(func[key][1][0], func[key][1][1])
                query = update.callback_query
                await query.answer()
                if mes:
                    [
                        await query.message.reply_text(el)
                        if lang == "eng"
                        else await query.message.reply_text(translate(el))
                        for el in mes
                    ]
                else:
                    await query.message.reply_text("I have found nothing(((")
            else:
                mes = f()
            await update.message.reply_text(
                mes
            ) if lang == "eng" else await update.message.reply_text(translate(mes))
