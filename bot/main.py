from . import middlewares
from .handlers import *
from .bot import dp

from aiogram import executor


def main(loop):
    dp.middleware.setup(middlewares.DBMiddleware())

    executor.start_polling(dp, skip_updates=False, loop=loop)
