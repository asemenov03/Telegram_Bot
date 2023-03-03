from aiogram import Dispatcher, types

from config import admin, bot_id, chat_id_zel
from create_bot import bot


async def text(message: types.Message):
    if message.chat.id == chat_id_zel and message.from_user.id != bot_id:
        if message.from_user.id != admin:
            await message.delete()
            await bot.send_message(chat_id=chat_id_zel, text='Отправка сообщений запрещена. Напишите боту',
                                   disable_notification=True)


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(text, lambda _: True)
