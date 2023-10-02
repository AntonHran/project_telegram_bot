from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from src.services.constants import QUOTE_TIME
from src.services.next_state import next_state_new


async def quote_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ans = update.message.text
    if ans and ans != "skip":
        context.user_data["menu_categories"][int(QUOTE_TIME)].append(ans.strip())
    elif ans == "skip":
        context.user_data["menu_categories"][int(QUOTE_TIME)].append("default")
    return await next_state_new(update, context)


quote_handler = MessageHandler(filters.TEXT, quote_time)
