import json
from pathlib import Path

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from aiofiles import open
from googletranslatepy import Translator

from src.services.constants import keys_


def translate(text: str) -> str:
    trnas = Translator()
    if len(text) < 5000:
        text = trnas.translate(text)
        return text
    else:
        text = [text[i: i + 5000] for i in range(0, len(text), 5000)]
        return "".join(text)


async def get_json(filepath: Path):
    async with open(filepath, "r", encoding="utf-8") as fr:
        return json.loads(await fr.read())


async def next_state_new(update, context):
    print(Path(__file__).parent.joinpath("languages.json"))
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
    return ConversationHandler.END


async def check(menu_category, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang_dict = await get_json(Path(__file__).parent.joinpath("languages.json"))
    lang = context.user_data["lang"]
    if (
        int(menu_category) in context.user_data["menu_categories"].keys()
        and not context.user_data["menu_categories"][int(menu_category)]
    ):
        await update.message.reply_text(
            text=lang_dict[lang]["phr"][keys_[menu_category]]
        )
        print(menu_category)
        return menu_category
