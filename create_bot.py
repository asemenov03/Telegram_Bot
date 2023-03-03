from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()
bot = Bot(token=config.zel_key_api_main)
dp = Dispatcher(bot, storage=storage)
