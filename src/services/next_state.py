from pathlib import Path

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from src.services.constants import keys_, NEWS, BOOKS
from src.services.assist_functions import get_json
from src.repository.news import news_category_choose
from src.repository.book import genres_choose


func = {
    NEWS: news_category_choose,
    BOOKS: genres_choose,
}


async def next_state_new(update, context):
    lang_dict = await get_json(Path(__file__).parent.joinpath("languages.json"))
    lang = context.user_data["lang"]
    for el in keys_:
        state = await check(el, update, context)
        if state:
            return state
    else:
        if update.message:
            await update.message.reply_text(text=lang_dict[lang]["phr"]["end_set"])
        else:
            query = update.callback_query
            await query.message.reply_text(text=lang_dict[lang]["phr"]["end_set"])
    print(context.user_data)
    return ConversationHandler.END


async def check(menu_category, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang_dict = await get_json(Path(__file__).parent.joinpath("languages.json"))
    lang = context.user_data["lang"]
    if (
        int(menu_category) in context.user_data["menu_categories"].keys()
        and not context.user_data["menu_categories"][int(menu_category)]
        and int(menu_category) not in func.keys()
    ):
        if update.message:
            await update.message.reply_text(text=lang_dict[lang]["phr"][keys_[menu_category]])
        else:
            query = update.callback_query
            await query.message.reply_text(text=lang_dict[lang]["phr"][keys_[menu_category]])
        print(menu_category)
        return menu_category
    elif (
        int(menu_category) in context.user_data["menu_categories"].keys() and
        int(menu_category) in func.keys() and
        not context.user_data["menu_categories"][int(menu_category)]
    ):
        return await func[menu_category](update, context)
