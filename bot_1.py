import datetime
import json
import logging

import telegram
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
)

from functions import (
    get_api_key,
    translate,
    form_quote,
    form_article,
    form_weather,
    form_news,
    form_books,
    form_trends,
)


TOKEN = get_api_key("token")
BOT_USERNAME = "@primary_trial_bot"

logging.basicConfig(
    filename="app.log",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Commands
(
    SELECTING_ACTION,
    LANG,
    DONE,
    BOOKS,
    CHANGE_LANGUAGE,
    NEWS,
    ARTICLE_TIME,
    MOTIVATION_TIME,
    COUNTRY,
    CATEGORY,
    CITY_WEATHER,
    TRENDS,
) = range(12)
menu_categories = []
categories, countries = [], []
lang = ""
data = {}

with open("languages.json", "r", encoding="utf-8") as jf:
    lang_dict = json.load(jf)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text=lang_dict[lang]["help"])


async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text=lang_dict[lang]["search"])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu_categories.clear()
    context.user_data.clear()
    await update.message.reply_text(f"Hello {update.message.from_user.name}!")
    button_lang = [[KeyboardButton(text="ENGLISH"), KeyboardButton(text="УКРАЇНСЬКА")]]
    reply_lang = ReplyKeyboardMarkup(
        button_lang, resize_keyboard=True, one_time_keyboard=True
    )
    await update.message.reply_text(
        "Please choose a language you would like to speak with me and receive messages. / "
        "Будь ласка оберіть мову котрою Ви би хотіли спілкуватися зі мною та отримувати "
        "сповіщення.",
        reply_markup=reply_lang,
    )
    return LANG


async def lang_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global lang
    lang = "eng" if update.message.text == "ENGLISH" else "ukr"
    print(f"lang: {lang}")
    await update.message.reply_text(
        "You have chosen English. LONG LIVE the KING!"
        if lang == "eng"
        else "Ви обрали українську мову. СЛАВА УКРАЇНІ!",
        reply_markup=telegram.ReplyKeyboardRemove(),
    )
    buttons_menu = [
        [
            telegram.InlineKeyboardButton(
                text=lang_dict[lang]["keys"]["motivation"],
                callback_data=str(MOTIVATION_TIME),
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
    print(menu)
    await query.answer()
    # await query.edit_message_reply_markup(reply_markup=telegram.InlineKeyboardMarkup([[telegram.InlineKeyboardButton(text='✔️ '+lang_dict[lang]['keys'][keys[int(menu)]])]]))  # '✔️'
    global chat_id_
    chat_id_ = query.message.chat_id
    data.update(
        {
            chat_id_: dict(
                name=query.from_user.name,
                article=[],
                books=[],
                motivation=[],
                lang="eng" if lang == "eng" else "ukr",
                news={"category": [], "country": []},
                trends=[],
                weather=[],
            )
        }
    )
    if menu == str(DONE):
        await query.message.reply_text(
            text=f"{lang_dict[lang]['phr']['cat_chosen']} "
            f"{', '.join([lang_dict[lang]['keys'][keys[cat]] for cat in menu_categories])}"
        )

        button_cont = [[KeyboardButton(text=lang_dict[lang]["keys"]["cont"])]]
        reply = ReplyKeyboardMarkup(
            button_cont, resize_keyboard=True, one_time_keyboard=True
        )
        await query.message.reply_text(
            text=lang_dict[lang]["phr"]["continue"][0], reply_markup=reply
        )
        return ConversationHandler.END
    menu_categories.append(int(menu))
    return SELECTING_ACTION


async def next_state_func(update, context) -> int:
    # print(context.user_data)
    if (
        str(MOTIVATION_TIME) in context.user_data.keys()
        and context.user_data[str(MOTIVATION_TIME)][1] != "done"
    ):
        await update.message.reply_text(text=lang_dict[lang]["phr"]["motivation"])
        context.user_data[str(MOTIVATION_TIME)][1] = "done"
        return MOTIVATION_TIME
    elif (
        str(ARTICLE_TIME) in context.user_data.keys()
        and context.user_data[str(ARTICLE_TIME)][1] != "done"
    ):
        await update.message.reply_text(text=lang_dict[lang]["phr"]["wiki"])
        context.user_data[str(ARTICLE_TIME)][1] = "done"
        return ARTICLE_TIME
    elif (
        str(CITY_WEATHER) in context.user_data.keys()
        and context.user_data[str(CITY_WEATHER)][1] != "done"
    ):
        await update.message.reply_text(text=lang_dict[lang]["phr"]["weather"])
        context.user_data[str(CITY_WEATHER)][1] = "done"
        return CITY_WEATHER
    elif (
        str(TRENDS) in context.user_data.keys()
        and context.user_data[str(TRENDS)][1] != "done"
    ):
        await update.message.reply_text(text=lang_dict[lang]["phr"]["twitter_trends"])
        context.user_data[str(TRENDS)][1] = "done"
        return TRENDS
    elif (
        str(BOOKS) in context.user_data.keys()
        and context.user_data[str(BOOKS)][1] != "done"
    ):
        await update.message.reply_text(text=lang_dict[lang]["phr"]["books"])
        context.user_data[str(BOOKS)][1] = "done"
        return BOOKS
    elif (
        str(CATEGORY) in context.user_data.keys()
        and context.user_data[str(CATEGORY)][1] != "done"
    ):
        countries.clear()
        categories.clear()
        buttons_category = [
            [
                telegram.InlineKeyboardButton(
                    text=lang_dict[lang]["keys"]["business"], callback_data="business"
                )
            ],
            [
                telegram.InlineKeyboardButton(
                    text=lang_dict[lang]["keys"]["entert"],
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
            text=lang_dict[lang]["phr"]["category"], reply_markup=reply
        )
        context.user_data[str(CATEGORY)][1] = "done"
        return CATEGORY
    else:
        print(data)

        # chat_id = list(data.keys())[0]  # update.message.chat_id
        """ with open('users.json', 'r') as jf:
            users = json.load(jf)
            if str(chat_id_) not in users.keys():
                users.update(data)
                with open('users.json', 'w') as f:
                    json.dump(users, f, indent=4)
            else:
                users.pop(str(chat_id_))
                users.update(data)
                with open('users.json', 'w') as f:
                    json.dump(users, f, indent=4)"""
        if update.message:
            await update.message.reply_text(text=lang_dict[lang]["phr"]["end_set"])
        else:
            query = update.callback_query
            await query.message.reply_text(text=lang_dict[lang]["phr"]["end_set"])
        await form_message(update, context)
        return ConversationHandler.END


async def continue_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text=lang_dict[lang]["phr"]["continue"][1],
        reply_markup=telegram.ReplyKeyboardRemove(),
    )
    for el in menu_categories:
        if el in keys:
            context.user_data[str(el)] = [el, True]
        if el == NEWS:
            context.user_data[str(CATEGORY)] = [CATEGORY, True]
    next_state = await next_state_func(update, context)
    return next_state


async def article_time(update, context):
    # chat_id = update.message.chat_id
    ans = update.message.text
    data[chat_id_]["article"].append(True)
    if ans and ans != "skip":
        data[chat_id_]["article"].append(
            datetime.datetime.strptime(ans.strip(), "%H:%M").time()
        )
    elif ans == "skip":
        data[chat_id_]["article"].append(
            datetime.datetime.strptime("9:00", "%H:%M").time()
        )
    next_state = await next_state_func(update, context)
    return next_state


async def set_time_mot(update, context):
    ans = update.message.text
    # chat_id = update.message.chat_id
    data[chat_id_]["motivation"].append(True)
    if ans and ans != "skip":
        data[chat_id_]["motivation"].append(
            datetime.datetime.strptime(ans, "%H:%M").time()
        )
    elif ans == "skip":
        data[chat_id_]["motivation"].append(
            datetime.datetime.strptime("9:00", "%H:%M").time()
        )
    next_state = await next_state_func(update, context)
    return next_state


async def category_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    category = query.data
    await query.answer()
    # await query.edit_message_text(text='✔️ ' + lang_dict[lang]['keys'][category])
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
    categories.append(category)
    return CATEGORY


async def country_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    country = query.data
    await query.answer()
    # await query.edit_message_text(text='✔️ ' + lang_dict[lang]['keys'][country])
    # chat_id = query.message.chat_id
    if country == "done":
        data[chat_id_]["news"]["category"] = categories
        data[chat_id_]["news"]["country"] = countries
        next_state = await next_state_func(update, context)
        return next_state
    countries.append(country)
    return COUNTRY


async def city_weather_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ans = update.message.text
    # chat_id = update.message.chat_id
    data[chat_id_]["weather"].append(True)
    if ans:
        data[chat_id_]["weather"].append(ans)
        next_state = await next_state_func(update, context)
        return next_state


async def trends_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ans = update.message.text
    # chat_id = update.message.chat_id
    data[chat_id_]["trends"].append(ans)
    next_state = await next_state_func(update, context)
    return next_state


async def books_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ans = update.message.text
    # chat_id = update.message.chat_id
    data[chat_id_]["books"].append((True, ans))
    next_state = await next_state_func(update, context)
    return next_state


async def cancel_settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(text=lang_dict[lang]["phr"]["cancel"])
    return ConversationHandler.END


async def form_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    func = get_access(chat_id_)
    # print(func)
    for key, value in data[chat_id_].items():
        if key in func and func[key][1]:
            # print(key, '|', func[key][1], type(func[key][1]))
            f = func[key][0]
            if type(func[key][1]) is datetime.time or type(func[key][1]) is str:
                # print(type(func[key][1]), '1')
                arg = func[key][1]
                mes = f(arg)
            elif type(func[key][1]) is list:
                # print(func[key][1][0], func[key][1][1])
                mes = f(func[key][1][0], func[key][1][1])
                # print(mes)
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
                # print('I am here')
                mes = f()
            # print(mes)
            await update.message.reply_text(
                mes
            ) if lang == "eng" else await update.message.reply_text(translate(mes))


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error, context.user_data}")


keys = {
    ARTICLE_TIME: "wiki",
    MOTIVATION_TIME: "motivation",
    CATEGORY: "",
    NEWS: "news",
    CITY_WEATHER: "weather",
    TRENDS: "twitter_trends",
    BOOKS: "books",
}


def get_access(chat_id):
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


def main():
    print("Starting bot...")
    app = ApplicationBuilder().token(token=TOKEN).build()

    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("search", search_command))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANG: [MessageHandler(filters.TEXT, lang_chosen)],
            SELECTING_ACTION: [telegram.ext.CallbackQueryHandler(settings_chosen)],
        },
        fallbacks=[],
    )

    conv_handler_settings = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT, continue_)],
        states={
            ARTICLE_TIME: [MessageHandler(filters.TEXT, article_time)],
            MOTIVATION_TIME: [MessageHandler(filters.TEXT, set_time_mot)],
            CATEGORY: [telegram.ext.CallbackQueryHandler(category_chosen)],
            COUNTRY: [telegram.ext.CallbackQueryHandler(country_chosen)],
            CITY_WEATHER: [MessageHandler(filters.TEXT, city_weather_chosen)],
            TRENDS: [MessageHandler(filters.TEXT, trends_chosen)],
            BOOKS: [MessageHandler(filters.TEXT, books_chosen)],
        },
        fallbacks=[CommandHandler("cancel", cancel_settings)],
    )

    app.add_handler(conv_handler)
    app.add_handler(conv_handler_settings)

    app.add_error_handler(error)

    print("Polling...")
    app.run_polling(poll_interval=3)


if __name__ == "__main__":
    main()
