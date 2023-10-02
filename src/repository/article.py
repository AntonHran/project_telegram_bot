from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from src.services.next_state import next_state_new
from src.services.constants import ARTICLE_TIME


async def article_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ans = update.message.text
    if ans and ans != "skip":
        context.user_data["menu_categories"][int(ARTICLE_TIME)].append(ans.strip())
    elif ans == "skip":
        context.user_data["menu_categories"][int(ARTICLE_TIME)].append("default")
    return await next_state_new(update, context)


article_handler = MessageHandler(filters.TEXT, article_time)
