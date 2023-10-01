from pathlib import Path

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

from src.services.constants import (SELECTING_ACTION, LANG, ARTICLE_TIME, QUOTE_TIME, GENRE,
                                    COUNTRY, CATEGORY, CITY_WEATHER, TRENDS, BOOKS, NEWS)
from src.services.assist_functions import next_state_new, get_json
from src.config.config import settings
from src.repository.categories import handler_category, handler_lang
from src.repository.article import article_handler
from src.repository.quote import quote_handler
from src.repository.weather import weather_handler
from src.repository.trends import trends_handler
from src.repository.news import handler_news, handler_news_category, handler_news_country
from src.repository.book import genre_handler, books_handler


'''
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text=lang_dict[lang]["help"])


async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text=lang_dict[lang]["search"])'''


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Hello {update.message.from_user.name}!")
    context.user_data["username"] = update.message.from_user.name
    context.user_data["chat_id"] = update.message.from_user.id
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


async def continue_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(Path(__file__).parent.joinpath("./src/services/languages.json"))
    lang_dict = await get_json(Path(__file__).parent.joinpath("./src/services/languages.json"))
    lang = context.user_data["lang"]
    await update.message.reply_text(
        text=lang_dict[lang]["phr"]["continue"][1],
        reply_markup=telegram.ReplyKeyboardRemove(),
    )
    next_state = await next_state_new(update, context)
    return next_state


async def cancel_settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang_dict = await get_json(
        Path(__file__).parent.joinpath("./src/services/languages.json")
    )
    lang = context.user_data["lang"]
    await update.message.reply_text(text=lang_dict[lang]["phr"]["cancel"])
    return ConversationHandler.END


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error, context.user_data}")


def main():
    print("Starting bot...")
    app = ApplicationBuilder().token(token=settings.token).build()

    '''app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("search", search_command))'''

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANG: [handler_lang],
            SELECTING_ACTION: [handler_category],
        },
        fallbacks=[],
    )
    app.add_handler(conv_handler)

    conv_handler_settings = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT, continue_)],
        states={
            ARTICLE_TIME: [article_handler],
            QUOTE_TIME: [quote_handler],
            NEWS: [handler_news],
            COUNTRY: [handler_news_country],
            CATEGORY: [handler_news_category],
            CITY_WEATHER: [weather_handler],
            TRENDS: [trends_handler],
            GENRE: [books_handler],
            BOOKS: [genre_handler],
        },
        fallbacks=[CommandHandler("cancel", cancel_settings)],
    )

    app.add_handler(conv_handler_settings)

    app.add_error_handler(error)

    print("Polling...")
    app.run_polling(poll_interval=3)


if __name__ == "__main__":
    main()

'''
async def next_state_func(update, context) -> int:
    print(context.user_data)
    lang_dict = await get_json(Path("./src/services/languages.json"))
    lang = context.user_data["lang"]
    if (
        int(QUOTE_TIME) in context.user_data["menu_categories"].keys()
        and not context.user_data["menu_categories"][int(QUOTE_TIME)]  # "done" not in
    ):
        await update.message.reply_text(text=lang_dict[lang]["phr"]["motivation"])
        # context.user_data["menu_categories"][int(QUOTE_TIME)].append("done")
        return QUOTE_TIME
    elif (
        int(ARTICLE_TIME) in context.user_data["menu_categories"].keys()
        and not context.user_data["menu_categories"][int(ARTICLE_TIME)]
    ):
        await update.message.reply_text(text=lang_dict[lang]["phr"]["wiki"])
        return ARTICLE_TIME
    elif (
        int(CITY_WEATHER) in context.user_data["menu_categories"].keys()
        and not context.user_data["menu_categories"][int(CITY_WEATHER)]
    ):
        await update.message.reply_text(text=lang_dict[lang]["phr"]["weather"])
        return CITY_WEATHER
    elif (
        int(TRENDS) in context.user_data["menu_categories"].keys()
        and not context.user_data["menu_categories"][int(TRENDS)]
    ):
        await update.message.reply_text(text=lang_dict[lang]["phr"]["twitter_trends"])
        return TRENDS
    elif (
        int(BOOKS) in context.user_data["menu_categories"].keys()
        and not context.user_data["menu_categories"][int(BOOKS)]
    ):
        await update.message.reply_text(text=lang_dict[lang]["phr"]["books"])
        return BOOKS
    elif (
        int(NEWS) in context.user_data["menu_categories"].keys()
        and not context.user_data["menu_categories"][int(NEWS)]
    ):
        await update.message.reply_text(text=lang_dict[lang]["phr"]["news"])
        return NEWS
    else:
        if update.message:
            await update.message.reply_text(text=lang_dict[lang]["phr"]["end_set"])
        else:
            query = update.callback_query
            await query.message.reply_text(text=lang_dict[lang]["phr"]["end_set"])
        # await form_message(update, context)
        return ConversationHandler.END


async def next_state_new(update, context):
    for el in keys:
        state = await check(el, update, context)
        if state:
            return state
    return ConversationHandler.END


async def check(menu_category, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang_dict = await get_json(Path("./src/services/languages.json"))
    lang = context.user_data["lang"]
    if int(menu_category) in context.user_data["menu_categories"].keys() and not context.user_data["menu_categories"][int(TRENDS)]:
        await update.message.reply_text(text=lang_dict[lang]["phr"][keys[menu_category]])
        return menu_category'''
