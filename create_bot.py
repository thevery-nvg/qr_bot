from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import Config

storage = MemoryStorage()
bot = Bot(Config.TG_TOKEN)
dp = Dispatcher(bot=bot, storage=storage)
