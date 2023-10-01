from pathlib import Path

from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from src.services.constants import QUOTE_TIME
from src.services.assist_functions import get_json, next_state_new


async def quote_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ans = update.message.text
    if ans and ans != "skip":
        context.user_data["menu_categories"][int(QUOTE_TIME)].append(ans.strip())
    elif ans == "skip":
        context.user_data["menu_categories"][int(QUOTE_TIME)].append("default")
    lang_dict = await get_json(Path(__file__).parent.parent.joinpath("services/languages.json"))
    # await update.message.reply_text(text=lang_dict[context.user_data["lang"]]["phr"]["motivation"])
    return await next_state_new(update, context)


quote_handler = MessageHandler(filters.TEXT, quote_time)
