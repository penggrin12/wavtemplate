from .db import users_db

from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message


class DBMiddleware(BaseMiddleware):
    """This is very ugly, and i dont know how to do this properly."""

    async def on_pre_process_message(self, message: Message, _):
        await users_db.make_sure_valid(message.from_user.id)
