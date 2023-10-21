from ..bot import dp

from aiogram import types


@dp.callback_query_handler(text="hello")
async def call_hello(call: types.CallbackQuery):
    await call.message.edit_text("🧸")