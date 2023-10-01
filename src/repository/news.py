from pathlib import Path

import telegram
from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler, ConversationHandler, MessageHandler, filters  # CallbackContext, JobQueue

from src.services.constants import COUNTRY, CATEGORY, NEWS
from src.services.assist_functions import get_json, next_state_new


async def news_category_choose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data["lang"]
    lang_dict = await get_json(Path(__file__).parent.parent.joinpath("services/languages.json"))
    context.user_data["menu_categories"][int(NEWS)] = {"news_categories": [], "news_countries": []}
    buttons_category = [
        [
            telegram.InlineKeyboardButton(
                text=lang_dict[lang]["keys"]["business"], callback_data="business"
            )
        ],
        [
            telegram.InlineKeyboardButton(
                text=lang_dict[lang]["keys"]["entertainment"],
                callback_data="entertainment",
            )
        ],
        [
            telegram.InlineKeyboardButton(
                text=lang_dict[lang]["keys"]["general"], callback_data="general"
            )
        ],
        [
            telegram.InlineKeyboardButton(
                text=lang_dict[lang]["keys"]["health"], callback_data="health"
            )
        ],
        [
            telegram.InlineKeyboardButton(
                text=lang_dict[lang]["keys"]["science"], callback_data="science"
            )
        ],
        [
            telegram.InlineKeyboardButton(
                text=lang_dict[lang]["keys"]["sports"], callback_data="sports"
            )
        ],
        [
            telegram.InlineKeyboardButton(
                text=lang_dict[lang]["keys"]["tech"], callback_data="technology"
            )
        ],
        [
            telegram.InlineKeyboardButton(
                text=lang_dict[lang]["keys"]["dn_c"], callback_data="done"
            )
        ],
    ]
    reply = telegram.InlineKeyboardMarkup(inline_keyboard=buttons_category)
    await update.message.reply_text(
        text=lang_dict[lang]["phr"]["news"], reply_markup=reply
    )
    return CATEGORY


async def category_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang_dict = await get_json(
        Path(__file__).parent.parent.joinpath("services/languages.json")
    )
    lang = context.user_data["lang"]
    query = update.callback_query
    category = query.data
    await query.answer()

    if category == "done":
        buttons_country = [
            [
                telegram.InlineKeyboardButton(
                    text=lang_dict[lang]["keys"]["ukr"], callback_data="ua"
                )
            ],
            [
                telegram.InlineKeyboardButton(
                    text=lang_dict[lang]["keys"]["usa"], callback_data="us"
                )
            ],
            [
                telegram.InlineKeyboardButton(
                    text=lang_dict[lang]["keys"]["ger"], callback_data="gr"
                )
            ],
            [
                telegram.InlineKeyboardButton(
                    text=lang_dict[lang]["keys"]["gb"], callback_data="gb"
                )
            ],
            [
                telegram.InlineKeyboardButton(
                    text=lang_dict[lang]["keys"]["fr"], callback_data="fr"
                )
            ],
            [
                telegram.InlineKeyboardButton(
                    text=lang_dict[lang]["keys"]["itl"], callback_data="it"
                )
            ],
            [
                telegram.InlineKeyboardButton(
                    text=lang_dict[lang]["keys"]["pld"], callback_data="pl"
                )
            ],
            [
                telegram.InlineKeyboardButton(
                    text=lang_dict[lang]["keys"]["dn_c"], callback_data="done"
                )
            ],
        ]
        await query.message.reply_text(
            text=lang_dict[lang]["phr"]["country"],
            reply_markup=telegram.InlineKeyboardMarkup(buttons_country),
        )
        return COUNTRY
    context.user_data["menu_categories"][int(NEWS)]["news_categories"].append(category)
    return CATEGORY


async def country_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    country = query.data
    await query.answer()
    if country == "done":
        # return ConversationHandler.END
        next_state = await next_state_new(update, context)
        return next_state
    context.user_data["menu_categories"][int(NEWS)]["news_countries"].append(country)
    return COUNTRY


handler_news = MessageHandler(filters.TEXT, news_category_choose)
# handler_news = MessageHandler(filters.TEXT & ~filters.COMMAND, some_handler)
handler_news_country = CallbackQueryHandler(country_chosen)
handler_news_category = CallbackQueryHandler(category_chosen)

news_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.TEXT, news_category_choose)],
    states={CATEGORY: [CallbackQueryHandler(category_chosen)],
            COUNTRY: [CallbackQueryHandler(country_chosen)]},
    fallbacks=[]
)
