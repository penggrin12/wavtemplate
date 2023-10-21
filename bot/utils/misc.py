import asyncio
import typing
import os.path
import random

from aiogram import types
from aiogram.utils.exceptions import RetryAfter

HINTS = ["Крутим шансы...", "Ставим шах и мат...", "Купаемся в вавах...",
         "Дорисовываем циферки...", "Гладим Святоша...", "Делаем баги..."]


async def try_edit(message: types.Message, text: str):
    try:
        await message.edit_text(text)
    except RetryAfter as e:
        print(f"got fw for {e} on {message.chat.id}")
        await asyncio.sleep(e.timeout)
        await try_edit(message, text)


# https://github.com/williexu/random_username
def generate_username(user_id: typing.Optional[int] = None):
    """Not really random, so this is not anonymous."""
    random.seed(user_id)

    directory_path = os.path.dirname(__file__)
    adjectives, nouns = [], []

    with open(os.path.join(directory_path, "..", "..", 'names_data', 'adjectives.txt'), 'r') as file_adjective:
        with open(os.path.join(directory_path, "..", "..", 'names_data', 'nouns.txt'), 'r') as file_noun:
            for line in file_adjective:
                adjectives.append(line.strip())

            for line in file_noun:
                nouns.append(line.strip())

    adjective = random.choice(adjectives)
    noun = random.choice(nouns).capitalize()
    num = str(random.randrange(10))
    result = adjective + noun + num

    random.seed()

    return result
