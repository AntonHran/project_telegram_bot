from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from src.services.constants import TRENDS
from src.services.next_state import next_state_new


async def trends_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ans = update.message.text
    if ans:
        context.user_data["menu_categories"][int(TRENDS)].append(ans.strip())
        next_state = await next_state_new(update, context)
        return next_state


trends_handler = MessageHandler(filters.TEXT, trends_chosen)
