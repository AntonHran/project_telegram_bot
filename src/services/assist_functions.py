import json
from pathlib import Path

from aiofiles import open
from googletranslatepy import Translator


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
