from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import bot
from keyboards import clubs, back_button_admin, kb_client4, next_button
import config


user = None


class FSMAdmin(StatesGroup):
    state1 = State()
    state2 = State()
    state3 = State()
    state4 = State()


async def cm_start(message: types.Message):
    await FSMAdmin.state1.set()
    await bot.send_message(message.from_user.id, 'Выберите город, в котором хотите выписать штраф',
                           reply_markup=clubs)


async def get_state1(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.finish()
        await bot.send_message(message.from_user.id, 'Здравствуйте', reply_markup=kb_client4)
    else:
        async with state.proxy() as data1:
            data1['state1'] = message.text
        await FSMAdmin.next()
        await bot.send_message(message.from_user.id, 'Прикрепите фото', reply_markup=next_button)


media = []


async def get_state2(message: types.Message, state: FSMContext):
    global media
    if message.text == "Назад":
        await FSMAdmin.state1.set()
        await bot.send_message(message.from_user.id, 'Выберите город, в котором хотите выписать штраф',
                               reply_markup=clubs)
    else:
        async with state.proxy() as data:
            if 'photos' in data.keys():
                data['photos'] = data['photos'].append(message.photo[-1].file_id)
            else:
                data['photos'] = []
        print(data)
        await FSMAdmin.state3.set()


async def get_state3(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await FSMAdmin.state2.set()
        await bot.send_message(message.from_user.id, 'Прикрепите фото', reply_markup=back_button_admin)
    else:
        async with state.proxy() as data:
            photo_ids = data['photos']
        photo_group = types.MediaGroup()
        for file_id in photo_ids:
            photo_group.attach_photo(file_id)
        await bot.send_media_group(chat_id=config.chat_id_zel, media=photo_group)
        await FSMAdmin.state4.set()


async def get_state4(message: types.Message, state: FSMContext):
    global media
    if message.text == "Назад":
        await FSMAdmin.state3.set()
        await bot.send_message(message.from_user.id, 'Прикрепите фото', reply_markup=back_button_admin)
    else:
        async with state.proxy() as data1:
            data1['state2'] = message.text
        await state.finish()
        await bot.send_message(message.from_user.id, 'Штраф отправлен', reply_markup=kb_client4)
        if data1['state1'] == 'Зеленогорск':
            await bot.send_media_group(chat_id=config.chat_id_zel, media=media)
            media = []
        elif data1['state1'] == 'Санкт-Петербург':
            await bot.send_message(chat_id=config.chat_id_spb, text=f"{data1['photo']}\n{data1['state2']}")
        elif data1['state1'] == 'Екатеринбург':
            await bot.send_message(chat_id=config.chat_id_spb, text=f"{data1['photo']}\n{data1['state2']}")
        elif data1['state1'] == 'Новосибирск':
            await bot.send_message(chat_id=config.chat_id_spb, text=f"{data1['photo']}\n{data1['state2']}")
        elif data1['state1'] == 'Красноярск (Урванцева)':
            await bot.send_message(chat_id=config.chat_id_spb, text=f"{data1['photo']}\n{data1['state2']}")
        elif data1['state1'] == 'Красноярск (Качинская)':
            await bot.send_message(chat_id=config.chat_id_spb, text=f"{data1['photo']}\n{data1['state2']}")
        else:
            await FSMAdmin.state1.set()
            await bot.send_message(message.from_user.id, 'Город указан неверно, попробуйте еще раз', reply_markup=clubs)


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, text=['Выписать штраф'], state=None)
    dp.register_message_handler(get_state1, state=FSMAdmin.state1)
    dp.register_message_handler(get_state2, content_types=types.ContentType.ANY, state=FSMAdmin.state2)
    dp.register_message_handler(get_state3, state=FSMAdmin.state3)
    dp.register_message_handler(get_state4, state=FSMAdmin.state4)
