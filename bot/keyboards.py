from aiogram import types


async def start():
    result = types.InlineKeyboardMarkup()

    result.add(types.InlineKeyboardButton("💎 Профиль", callback_data="profile"))
    result.add(
        types.InlineKeyboardButton("💎 Пополнить", callback_data="deposit"),
        types.InlineKeyboardButton("💎 Вывести", callback_data="withdraw"),
    )
    result.add(types.InlineKeyboardButton("🐻 Привет", callback_data="hello"))

    return result


async def profile():
    result = types.InlineKeyboardMarkup()

    result.add(
        types.InlineKeyboardButton("💎 Пополнить", callback_data="deposit"),
        types.InlineKeyboardButton("💎 Вывести", callback_data="withdraw"),
    )
    result.add(types.InlineKeyboardButton("Назад", callback_data="start"))

    return result


async def deposit():
    result = types.InlineKeyboardMarkup()

    result.add(types.InlineKeyboardButton("Отмена", callback_data="profile"))

    return result


async def deposit_end():
    result = types.InlineKeyboardMarkup()

    result.add(types.InlineKeyboardButton("В меню", callback_data="start"))

    return result


async def withdraw():
    result = types.InlineKeyboardMarkup()

    result.add(types.InlineKeyboardButton("Отмена", callback_data="profile"))

    return result
