from pathlib import Path

import telegram
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters, ConversationHandler

from src.services.constants import (
    SELECTING_ACTION,
    QUOTE_TIME,
    CITY_WEATHER,
    TRENDS,
    ARTICLE_TIME,
    NEWS,
    BOOKS,
    CHANGE_LANGUAGE,
    DONE,
    keys_
)
from src.services.assist_functions import get_json


async def lang_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["lang"] = "eng" if update.message.text == "ENGLISH" else "ukr"
    context.user_data["menu_categories"] = {}
    lang = context.user_data["lang"]
    await update.message.reply_text(
        "You have chosen English. LONG LIVE the KING!"
        if lang == "eng"
        else "Ви обрали українську мову. СЛАВА УКРАЇНІ!",
        reply_markup=telegram.ReplyKeyboardRemove(),
    )
    lang_dict = await get_json(Path(__file__).parent.parent.joinpath('services/languages.json'))
    buttons_menu = [
        [
            telegram.InlineKeyboardButton(
                text=lang_dict[lang]["keys"]["motivation"],
                callback_data=str(QUOTE_TIME),
            ),
            telegram.InlineKeyboardButton(
                text=lang_dict[lang]["keys"]["weather"], callback_data=str(CITY_WEATHER)
            ),
        ],
        [
            telegram.InlineKeyboardButton(
                text=lang_dict[lang]["keys"]["twitter_trends"],
                callback_data=str(TRENDS),
            ),
            telegram.InlineKeyboardButton(
                text=lang_dict[lang]["keys"]["wiki"], callback_data=str(ARTICLE_TIME)
            ),
        ],
        [
            telegram.InlineKeyboardButton(
                text=lang_dict[lang]["keys"]["news"], callback_data=str(NEWS)
            ),
            telegram.InlineKeyboardButton(
                text=lang_dict[lang]["keys"]["books"], callback_data=str(BOOKS)
            ),
        ],
        [
            telegram.InlineKeyboardButton(
                text=lang_dict[lang]["keys"]["change_language"],
                callback_data=str(CHANGE_LANGUAGE),
            )
        ],
        [
            telegram.InlineKeyboardButton(
                text=lang_dict[lang]["keys"]["done"], callback_data=str(DONE)
            )
        ],
    ]
    reply = telegram.InlineKeyboardMarkup(inline_keyboard=buttons_menu)
    await update.message.reply_text(
        text=lang_dict[lang]["phr"]["set"], reply_markup=reply
    )
    return SELECTING_ACTION


async def settings_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    menu = query.data
    await query.answer()
    if menu == str(DONE):
        lang_dict = await get_json(Path(__file__).parent.parent.joinpath('services/languages.json'))
        lang = context.user_data['lang']
        await query.message.reply_text(
            text=f"{lang_dict[lang]['phr']['cat_chosen']} "
            f"{', '.join([lang_dict[lang]['keys'][keys_[cat]] for cat in context.user_data['menu_categories'].keys()])}"
        )

        button_cont = [[KeyboardButton(text=lang_dict[lang]["keys"]["cont"])]]
        reply = ReplyKeyboardMarkup(
            button_cont, resize_keyboard=True, one_time_keyboard=True
        )
        await query.message.reply_text(
            text=lang_dict[lang]["phr"]["continue"][0], reply_markup=reply
        )
        return ConversationHandler.END
    context.user_data["menu_categories"].update({int(menu): []})
    return SELECTING_ACTION


handler_lang = MessageHandler(filters.TEXT, lang_chosen)
handler_category = telegram.ext.CallbackQueryHandler(settings_chosen)

'''conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANG: [MessageHandler(filters.TEXT, lang_chosen)],
            SELECTING_ACTION: [telegram.ext.CallbackQueryHandler(settings_chosen)],
        },
        fallbacks=[],
    )
'''
