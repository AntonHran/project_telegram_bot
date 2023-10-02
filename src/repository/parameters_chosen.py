from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler

from src.services.constants import COUNTRY, NEWS, GENRE, BOOKS
from src.services.next_state import next_state_new


async def country_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    country = query.data
    await query.answer()
    if country == "done":
        next_state = await next_state_new(update, context)
        return next_state
    context.user_data["menu_categories"][int(NEWS)]["news_countries"].append(country)
    return COUNTRY


handler_news_country = CallbackQueryHandler(country_chosen)


async def genre_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    genre = query.data
    await query.answer()
    if genre == "done":
        next_state = await next_state_new(update, context)
        return next_state
    context.user_data["menu_categories"][int(BOOKS)].append(genre)
    return GENRE


books_handler = CallbackQueryHandler(genre_chosen)
