from pathlib import Path

from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from src.services.assist_functions import get_json, next_state_new
from src.services.constants import ARTICLE_TIME


async def article_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ans = update.message.text
    if ans and ans != "skip":
        context.user_data["menu_categories"][int(ARTICLE_TIME)].append(ans.strip())
    elif ans == "skip":
        context.user_data["menu_categories"][int(ARTICLE_TIME)].append("default")
    lang_dict = await get_json(Path(__file__).parent.parent.joinpath("services/languages.json"))
    await update.message.reply_text(text=lang_dict[context.user_data["lang"]]["phr"]["wiki"])
    return await next_state_new(update, context)


article_handler = MessageHandler(filters.TEXT, article_time)
