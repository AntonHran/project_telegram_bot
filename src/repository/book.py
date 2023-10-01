from pathlib import Path

import telegram
from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler, MessageHandler, filters

from src.services.constants import GENRE, BOOKS
from src.services.assist_functions import next_state_new, get_json


async def genres_choose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang_dict = await get_json(Path(__file__).parent.parent.joinpath("services/languages.json"))
    lang = context.user_data["lang"]
    buttons_genres = [
        [
            telegram.InlineKeyboardButton(
                text=lang_dict[lang]["keys"]["fiction"], callback_data="fiction"
            )
        ],
        [
            telegram.InlineKeyboardButton(
                text=lang_dict[lang]["keys"]["mystery"], callback_data="mystery"
            )
        ],
        [
            telegram.InlineKeyboardButton(
                text=lang_dict[lang]["keys"]["science fiction"], callback_data="science fiction"
            )
        ],
        [
            telegram.InlineKeyboardButton(
                text=lang_dict[lang]["keys"]["fantasy"], callback_data="fantasy"
            )
        ],
        [
            telegram.InlineKeyboardButton(
                text=lang_dict[lang]["keys"]["romance"], callback_data="romance"
            )
        ],
        [
            telegram.InlineKeyboardButton(
                text=lang_dict[lang]["keys"]["adventure"], callback_data="adventure"
            )
        ],
        [
            telegram.InlineKeyboardButton(
                text=lang_dict[lang]["keys"]["biography"], callback_data="biography"
            )
        ],
        [
            telegram.InlineKeyboardButton(
                text=lang_dict[lang]["keys"]["non-fiction"], callback_data="non-fiction"
            )
        ],
        [
            telegram.InlineKeyboardButton(
                text=lang_dict[lang]["keys"]["horror"], callback_data="horror"
            )
        ],
        [
            telegram.InlineKeyboardButton(
                text=lang_dict[lang]["keys"]["thriller"], callback_data="thriller"
            )
        ],
        [
            telegram.InlineKeyboardButton(
                text=lang_dict[lang]["keys"]["comedy"], callback_data="comedy"
            )
        ],
        [
            telegram.InlineKeyboardButton(
                text=lang_dict[lang]["keys"]["drama"], callback_data="drama"
            )
        ],
        [
            telegram.InlineKeyboardButton(
                text=lang_dict[lang]["keys"]["dn_c"], callback_data="done"
            )
        ],
    ]
    await update.message.reply_text(
        text=lang_dict[lang]["phr"]["books"],
        reply_markup=telegram.InlineKeyboardMarkup(buttons_genres),
    )
    return GENRE


async def genre_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    genre = query.data
    await query.answer()
    if genre == "done":
        next_state = await next_state_new(update, context)
        return next_state
    context.user_data["menu_categories"][int(BOOKS)].append(genre)
    return GENRE


genre_handler = MessageHandler(filters.TEXT, genres_choose)
books_handler = CallbackQueryHandler(genre_chosen)
