from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from src.services.constants import CITY_WEATHER
from src.services.assist_functions import next_state_new


async def city_weather_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ans = update.message.text
    if ans:
        context.user_data["menu_categories"][int(CITY_WEATHER)].append(ans)
        next_state = await next_state_new(update, context)
        return next_state


weather_handler = MessageHandler(filters.TEXT, city_weather_chosen)
