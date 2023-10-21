from .loops import loop
from .config import BOT_TOKEN

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=BOT_TOKEN, parse_mode="html")
dp = Dispatcher(bot, loop=loop, storage=MemoryStorage())
