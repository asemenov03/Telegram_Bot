from datetime import datetime
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
import asyncio
import config


from create_bot import bot
from keyboards import kb_client1, kb_client2, kb_client3, back_button, client_out_button, back_button_admin, decision, clean1
from config import chat_id_zel, chat_id_ekb, chat_id_spb, chat_id_nsk, chat_id_krskk, chat_id_krsku


channels = {
    'Зеленогорск': chat_id_zel,
    'Екатеринбург': chat_id_ekb,
    'Санкт-Петербург': chat_id_spb,
    'Новосибирск': chat_id_nsk,
    'Урванцева': chat_id_krskk,
    'Качинская': chat_id_krsku
}

data1 = {}

chat_id_zel = config.chat_id_zel
user = None


#Заполнение отчета
class FSMClient(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()
    q5 = State()
    q6 = State()
    q7 = State()
    q8 = State()
    q9 = State()
    q10 = State()
    q11 = State()
    q12 = State()
    q13 = State()
    q14 = State()
    q15 = State()
    q16 = State()
    q17 = State()
    q18 = State()
    get_nonfunc_equipment = State()


async def command_start(message: types.Message):
    global channels, counter
    counter = 0
    for channel in channels:
        user_channel_status = await bot.get_chat_member(chat_id=channels[channel], user_id=message.from_user.id)
        if user_channel_status["status"] != 'left' and user_channel_status["status"] != 'kicked':
            data1[str(channels[channel])] = str(user_channel_status['user']['id'])
        usertg = await bot.get_chat_member(chat_id=channels[channel], user_id=message.from_user.id)
        if usertg.status == "member" or usertg.status == "creator" or usertg.status == "administrator":
            counter += 1
    if counter != 0:
        await bot.send_message(message.from_user.id, 'Здравствуйте', reply_markup=kb_client1)
    else:
        await bot.send_message(message.from_user.id, 'Вы не являетесь администратором',
                               reply_markup=ReplyKeyboardRemove())


# Начало первого состояния
# @dp.message_handler(text=['Дневная смена', 'Ночная_смена'])
async def day_night(message: types.Message):
    global channels, counter
    counter = 0
    for channel in channels:
        user_channel_status = await bot.get_chat_member(chat_id=channels[channel], user_id=message.from_user.id)
        if user_channel_status["status"] != 'left' and user_channel_status["status"] != 'kicked':
            data1[str(channels[channel])] = str(user_channel_status['user']['id'])
        usertg = await bot.get_chat_member(chat_id=channels[channel], user_id=message.from_user.id)
        if usertg.status == "member" or usertg.status == "creator" or usertg.status == "administrator":
            counter += 1
    if counter != 0:
        await FSMClient.q1.set()
        await bot.send_message(message.from_user.id, 'В какое время вы пришли на смену?',
                               reply_markup=client_out_button)
    else:
        await bot.send_message(message.from_user.id, 'Вы не являетесь администратором',
                               reply_markup=ReplyKeyboardRemove())


# Выход из состояния
# @dp.message_handlers(state='*', commands='отмена')
# @dp.message_handlers(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return None
    await state.finish()
    await bot.send_message(message.from_user.id, 'Вы вернулись в начальное меню', reply_markup=kb_client1)


# Первый ответ
# @dp.message_handler(state=FSMClient.q1)
async def q1(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await FSMClient.q1.set()
        await bot.send_message(message.from_user.id, 'Здравствуйте', reply_markup=kb_client1)
    else:
        async with state.proxy() as data:
            data['q1'] = message.text
        await FSMClient.next()
        await bot.send_message(message.from_user.id, 'Вы сделали обход заведения?', reply_markup=kb_client2)


# Второй ответ
# @dp.message_handler(state=FSMClient.q2)
async def q2(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await FSMClient.q1.set()
        await bot.send_message(message.from_user.id, 'В какое время вы пришли на смену?',
                               reply_markup=client_out_button)
    else:
        async with state.proxy() as data:
            data['q2'] = message.text
            if data['q2'] == "Да":
                await FSMClient.next()
                await bot.send_message(message.from_user.id, 'С какого устройства вы заполняете отчет?',
                                       reply_markup=kb_client3)
            elif data['q2'] == 'Нет':
                await bot.send_message(message.from_user.id, 'Сделайте обход. Я напишу вам через 5 минут',
                                       reply_markup=back_button)
                await asyncio.sleep(300)
                await FSMClient.q2.set()
                await bot.send_message(message.from_user.id, 'Вы сделали обход заведения?', reply_markup=kb_client2)
            else:
                await bot.send_message(message.from_user.id, 'Такой ответ не предусмотрен')
                await FSMClient.q2.set()
                await bot.send_message(message.from_user.id, 'Вы сделали обход заведения?', reply_markup=kb_client2)


# Третий ответ
# @dp.message_handler(state=FSMClient.q3)
async def q3(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await FSMClient.q2.set()
        await bot.send_message(message.from_user.id, 'Вы сделали обход заведения?', reply_markup=kb_client2)
    else:
        async with state.proxy() as data:
            data['q3'] = message.text
            if data['q3'] == "Компьютер":
                await FSMClient.next()
                await bot.send_message(message.from_user.id, 'Состояние кассы (ЛОКЕР)', reply_markup=back_button)
            elif data['q3'] == 'Телефон':
                await FSMClient.next()
                await bot.send_message(message.from_user.id, 'Состояние кассы (ЛОКЕР)', reply_markup=back_button)
            else:
                await bot.send_message(message.from_user.id, 'Такой ответ не предусмотрен')
                await FSMClient.q3.set()
                await bot.send_message(message.from_user.id, 'С какого устройства вы заполняете отчет?',
                                       reply_markup=kb_client3)


# Четвертый ответ
# @dp.message_handler(state=FSMClient.q4)
async def q4(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await FSMClient.q3.set()
        await bot.send_message(message.from_user.id, 'С какого устройства вы заполняете отчет?',
                               reply_markup=kb_client3)
    else:
        async with state.proxy() as data:
            data['q4'] = message.text
            await FSMClient.next()
            await bot.send_message(message.from_user.id, 'Кол-во системных блоков',
                                   reply_markup=back_button)


# Пятый ответ
# @dp.message_handler(state=FSMClient.q5)
async def q5(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await FSMClient.q4.set()
        await bot.send_message(message.from_user.id, 'Состояние кассы (ЛОКЕР)', reply_markup=back_button)
    else:
        async with state.proxy() as data:
            data['q5'] = message.text
            if data['q5'] == "100":
                pass
            elif int(data['q5']) < 100:
                pass
            else:
                pass
        await FSMClient.next()
        await bot.send_message(message.from_user.id, 'Кол-во мониторов', reply_markup=back_button)


# Шестой ответ
# @dp.message_handler(state=FSMClient.q6)
async def q6(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await FSMClient.q5.set()
        await bot.send_message(message.from_user.id, 'Кол-во системных блоков', reply_markup=back_button)
    else:
        async with state.proxy() as data:
            data['q6'] = message.text
            if data['q6'] >= "100":
                pass
            elif int(data['q6']) < 100:
                pass
            else:
                pass
        await FSMClient.next()
        await bot.send_message(message.from_user.id, 'Кол-во клавиатур',
                               reply_markup=back_button)


# Седьмой ответ
# @dp.message_handler(state=FSMClient.q7)
async def q7(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await FSMClient.q6.set()
        await bot.send_message(message.from_user.id, 'Кол-во мониторов',
                               reply_markup=back_button)
    else:
        async with state.proxy() as data:
            data['q7'] = message.text
            if data['q7'] == "100":
                pass
            elif int(data['q7']) < 100:
                pass
            else:
                pass
        await FSMClient.next()
        await bot.send_message(message.from_user.id, 'Кол-во наушников', reply_markup=back_button)


# Восьмой ответ
# @dp.message_handler(state=FSMClient.q8)
async def q8(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await FSMClient.q7.set()
        await bot.send_message(message.from_user.id, 'Кол-во клавиатур', reply_markup=back_button)
    else:
        async with state.proxy() as data:
            data['q8'] = message.text
            if data['q8'] == "100":
                pass
            elif int(data['q8']) < 100:
                pass
            else:
                pass
        await FSMClient.next()
        await bot.send_message(message.from_user.id, 'Кол-во мышек', reply_markup=back_button)


# Девятый ответ
async def q9(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await FSMClient.q8.set()
        await bot.send_message(message.from_user.id, 'Кол-во наушников', reply_markup=back_button)
    else:
        async with state.proxy() as data:
            data['q9'] = message.text
            if data['q9'] == "100":
                pass
            elif int(data['q9']) < 100:
                pass
            else:
                pass
        await FSMClient.next()
        await bot.send_message(message.from_user.id, 'Кол-во кресел', reply_markup=back_button)

# Десятый ответ
async def q10(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await FSMClient.q9.set()
        await bot.send_message(message.from_user.id, 'Кол-во мышек', reply_markup=back_button)
    else:
        async with state.proxy() as data:
            data['q10'] = message.text
            if data['q10'] == "100":
                pass
            elif int(data['q10']) < 100:
                pass
            else:
                pass
        await FSMClient.next()
        await bot.send_message(message.from_user.id, 'Укажите дополнительное оборудование ОДНИМ сообщением',
                               reply_markup=back_button)


# Одиннадцатый ответ
# @dp.message_handler(state=FSMClient.q9)
async def q11(message: types.Message, state: FSMContext):
    global data1
    if message.text == "Назад":
        await FSMClient.q10.set()
        await bot.send_message(message.from_user.id, 'Кол-во кресел', reply_markup=back_button)
    else:
        async with state.proxy() as data:
            data['q11'] = message.text
        await FSMClient.next()
        await bot.send_message(message.from_user.id, 'Кол-во рабочих системных блоков',
                               reply_markup=back_button)

# Двенадцатый ответ
async def q12(message: types.Message, state: FSMContext):
    global current_state
    current_state = await state.get_state()
    if message.text == "Назад":
        await FSMClient.q11.set()
        await bot.send_message(message.from_user.id, 'Укажите дополнительное оборудование ОДНИМ сообщением',
                               reply_markup=back_button)
    else:
        async with state.proxy() as data:
            data['q12'] = message.text
            if int(data['q12']) >= int(data['q5']):
                await FSMClient.next()
                await bot.send_message(message.from_user.id, 'Кол-во рабочих мониторов',
                                       reply_markup=back_button)
            elif int(data['q12']) < int(data['q5']):
                await bot.send_message(message.from_user.id,
                                       'Что не так с нерабочим оборудованием? Напишите ОДНИМ сообщением',
                                       reply_markup=back_button_admin)
                await FSMClient.get_nonfunc_equipment.set()
            else:
                pass


# Тринадцатый ответ
# @dp.message_handler(state=FSMClient.q5)
async def q13(message: types.Message, state: FSMContext):
    global current_state
    current_state = await state.get_state()
    if message.text == "Назад":
        await FSMClient.q12.set()
        await bot.send_message(message.from_user.id, 'Кол-во рабочих системных блоков',
                               reply_markup=back_button)
    else:
        async with state.proxy() as data:
            data['q13'] = message.text
            if int(data['q13']) >= int(data['q6']):
                await FSMClient.next()
                await bot.send_message(message.from_user.id, 'Кол-во рабочих клавиатур', reply_markup=back_button)
            elif int(data['q13']) < int(data['q6']):
                await bot.send_message(message.from_user.id,
                                       'Что не так с нерабочим оборудованием? Напишите ОДНИМ сообщением',
                                       reply_markup=back_button_admin)
                await FSMClient.get_nonfunc_equipment.set()
            else:
                pass


# Четырнадцатый ответ
# @dp.message_handler(state=FSMClient.q6)
async def q14(message: types.Message, state: FSMContext):
    global current_state
    current_state = await state.get_state()
    if message.text == "Назад":
        await FSMClient.q13.set()
        await bot.send_message(message.from_user.id, 'Кол-во рабочих мониторов',
                               reply_markup=back_button)
    else:
        async with state.proxy() as data:
            data['q14'] = message.text
            if int(data['q14']) >= int(data['q7']):
                await FSMClient.next()
                await bot.send_message(message.from_user.id, 'Кол-во рабочих наушников', reply_markup=back_button)
            elif int(data['q14']) < int(data['q7']):
                await bot.send_message(message.from_user.id,
                                       'Что не так с нерабочим оборудованием? Напишите ОДНИМ сообщением',
                                       reply_markup=back_button_admin)
                await FSMClient.get_nonfunc_equipment.set()
            else:
                pass


# Пятнадцатый ответ
# @dp.message_handler(state=FSMClient.q7)
async def q15(message: types.Message, state: FSMContext):
    global current_state
    current_state = await state.get_state()
    if message.text == "Назад":
        await FSMClient.q14.set()
        await bot.send_message(message.from_user.id, 'Кол-во рабочих клавиатур', reply_markup=back_button)
    else:
        async with state.proxy() as data:
            data['q15'] = message.text
            if int(data['q15']) >= int(data['q8']):
                await FSMClient.next()
                await bot.send_message(message.from_user.id, 'Кол-во рабочих мышек', reply_markup=back_button)
            elif int(data['q15']) < int(data['q8']):
                await bot.send_message(message.from_user.id,
                                       'Что не так с нерабочим оборудованием? Напишите ОДНИМ сообщением',
                                       reply_markup=back_button_admin)
                await FSMClient.get_nonfunc_equipment.set()
            else:
                pass


# Шестнадцатый ответ
# @dp.message_handler(state=FSMClient.q8)
async def q16(message: types.Message, state: FSMContext):
    global current_state
    current_state = await state.get_state()
    if message.text == "Назад":
        await FSMClient.q15.set()
        await bot.send_message(message.from_user.id, 'Кол-во рабочих наушников', reply_markup=back_button)
    else:
        async with state.proxy() as data:
            data['q16'] = message.text
            if int(data['q16']) >= int(data['q9']):
                await FSMClient.next()
                await bot.send_message(message.from_user.id, 'Кол-во рабочих кресел', reply_markup=back_button)
            elif int(data['q16']) < int(data['q9']):
                await bot.send_message(message.from_user.id,
                                       'Что не так с нерабочим оборудованием? Напишите ОДНИМ сообщением',
                                       reply_markup=back_button_admin)
                await FSMClient.get_nonfunc_equipment.set()
            else:
                pass


# Девятый ответ
async def q17(message: types.Message, state: FSMContext):
    global current_state
    current_state = await state.get_state()
    if message.text == "Назад":
        await FSMClient.q16.set()
        await bot.send_message(message.from_user.id, 'Кол-во рабочих мышек', reply_markup=back_button)
    else:
        async with state.proxy() as data:
            data['q17'] = message.text
            if int(data['q17']) >= int(data['q10']):
                await FSMClient.next()
                await bot.send_message(message.from_user.id,
                                       'Укажите рабочее дополнительное оборудование ОДНИМ сообщением',
                                       reply_markup=back_button)
            elif int(data['q17']) < int(data['q10']):
                await bot.send_message(message.from_user.id,
                                       'Что не так с нерабочим оборудованием? Напишите ОДНИМ сообщением',
                                       reply_markup=back_button_admin)
                await FSMClient.get_nonfunc_equipment.set()
            else:
                pass


async def q18(message: types.Message, state: FSMContext):
    global current_state
    current_state = await state.get_state()
    if message.text == "Назад":
        await FSMClient.q17.set()
        await bot.send_message(message.from_user.id, 'Кол-во мышек', reply_markup=back_button)
    else:
        async with state.proxy() as data:
            data['q18'] = message.text
        current_date = datetime.now()
        formatted_date = current_date.strftime("%d.%m.%y")
        async with state.proxy() as data:
            await bot.send_message(message.from_user.id, 'Спасибо за отчет. Не забудьте написать отчет по уборке',
                                   reply_markup=kb_client1)
            await bot.send_message(chat_id=chat_id_zel,
                                   text=f'Отчет за {formatted_date}\nВремя: {data["q1"]}\nАдминистратор'
                                        f' {message.from_user.first_name} {message.from_user.last_name}'
                                        f' (@{message.from_user.username})\nЛокер: {data["q4"]}\n\n'
                                        f'1. Оборудование:\n\nСистемные блоки: {data["q5"]}\nМониторы: '
                                        f'{data["q6"]}\nКлавиатуры: {data["q7"]}\nНаушники: {data["q8"]}\nМышки:'
                                        f' {data["q9"]}\nКресла: {data["q10"]}\n{data["q11"]}\n\n2. Неисправное'
                                        f' оборудование:\n\n3. Итог по рабочему оборудованию:\n\nСистемные блоки: '
                                        f'{data["q12"]}\nМониторы: {data["q13"]}\nКлавиатуры: {data["q14"]}\nНаушники:'
                                        f' {data["q15"]}\nМышки: {data["q16"]}\nКресла: {data["q17"]}\n{data["q18"]}\n\n')
        await state.finish()


count1 = 0


async def get_nonfunctioning_equipment(message: types.Message, state: FSMContext):
    global current_state
    global count1
    if message.text == "Назад":
        if current_state == 'FSMClient:q12':
            await FSMClient.q12.set()
            await bot.send_message(message.from_user.id, 'Кол-во рабочих системных блоков',
                                   reply_markup=back_button)
        elif current_state == 'FSMClient:q13':
            await FSMClient.q13.set()
            await bot.send_message(message.from_user.id,
                                   'Кол-во рабочих мониторов',
                                   reply_markup=back_button)
        elif current_state == 'FSMClient:q14':
            await FSMClient.q14.set()
            await bot.send_message(message.from_user.id,
                                   'Кол-во рабочих клавиатур',
                                   reply_markup=back_button)
        elif current_state == 'FSMClient:q15':
            await FSMClient.q15.set()
            await bot.send_message(message.from_user.id,
                                   'Кол-во рабочих наушников',
                                   reply_markup=back_button)
        elif current_state == 'FSMClient:q16':
            await FSMClient.q16.set()
            await bot.send_message(message.from_user.id,
                                   'Кол-во рабочих мышек',
                                   reply_markup=back_button)
        elif current_state == 'FSMClient:q17':
            await FSMClient.q17.set()
            await bot.send_message(message.from_user.id,
                                   'Кол-во рабочих кресел',
                                   reply_markup=back_button)
        elif current_state == 'FSMClient:q18':
            await FSMClient.q18.set()
            await bot.send_message(message.from_user.id, 'Кол-во мышек', reply_markup=back_button)
    else:
        async with state.proxy() as data:
            data[f'fanc{count1}'] = message.text
        print(data)
        count1 += 1


# Задерживаюсь на смену
class FSMClientLate(StatesGroup):
    q1 = State()
    q2 = State()


# @dp.message_handler(text=['Задерживаюсь на смену'])
async def late(message: types.Message):
    global channels, counter
    counter = 0
    for channel in channels:
        user_channel_status = await bot.get_chat_member(chat_id=channels[channel], user_id=message.from_user.id)
        if user_channel_status["status"] != 'left' and user_channel_status["status"] != 'kicked':
            data1[str(channels[channel])] = str(user_channel_status['user']['id'])
            # sqlite_db.sql_start(user_channel_status, channel, channels)
        # sqlite_db.data_main()
        user = await bot.get_chat_member(chat_id=channels[channel], user_id=message.from_user.id)
        if user.status == "member" or user.status == "creator" or user.status == "administrator":
            counter += 1
    if counter != 0:
        await FSMClientLate.q1.set()
        await bot.send_message(message.from_user.id, 'Напишите причину', reply_markup=client_out_button)
    else:
        await bot.send_message(message.from_user.id, 'Вы не являетесь администратором',
                               reply_markup=ReplyKeyboardRemove())


async def get_late1(message: types.Message, state: FSMContext):
    if message.chat.id == config.chat_id_zel and message.from_user.id != config.bot_id:
        await message.delete()
        return
    if message.text == "Назад":
        await FSMClientLate.q1.set()
        await bot.send_message(message.from_user.id, 'Здравствуйте', reply_markup=kb_client1)
    else:
        async with state.proxy() as data_late:
            data_late['q1'] = message.text
        await FSMClientLate.next()
        await bot.send_message(message.from_user.id,
                               'Вы хотите отправить причину опоздания в общий чат или конфиденциально?',
                               reply_markup=decision)


async def get_late2(message: types.Message, state: FSMContext):
    if message.chat.id == config.chat_id_zel and message.from_user.id != config.bot_id:
        await message.delete()
        return
    if message.text == "Назад":
        await FSMClientLate.q1.set()
        await bot.send_message(message.from_user.id, 'Напишите причину', reply_markup=client_out_button)
    else:
        async with state.proxy() as data_late:
            data_late['q2'] = message.text
        if data_late['q2'] == 'Отправить в общий чат':
            await bot.send_message(message.from_user.id, 'Сообщение отправлено', reply_markup=kb_client1)
            await bot.send_message(chat_id=-1001670247565,
                                   text=f'Администратор {message.from_user.first_name} {message.from_user.last_name}'
                                        f' (@{message.from_user.username}) задерживается на смену.\nПричина:'
                                        f' {data_late["q1"]}.')
        else:
            await bot.send_message(message.from_user.id, 'Сообщение отправлено', reply_markup=kb_client1)
            await bot.send_message(chat_id=-726791286,
                                   text=f'Администратор {message.from_user.first_name} {message.from_user.last_name}'
                                        f' (@{message.from_user.username}) задерживается на смену.\nПричина:'
                                        f' {data_late["q1"]}.')
        await state.finish()



# Отчет по уборке
class FSMClientClean(StatesGroup):
    yes_no = State()
    toilets = State()
    rooms = State()
    tables = State()
    reason = State()


current_state = None


# @dp.message_handler(text=['Задерживаюсь на смену'])
async def clean(message: types.Message):
    global channels, counter
    counter = 0
    for channel in channels:
        user_channel_status = await bot.get_chat_member(chat_id=channels[channel], user_id=message.from_user.id)
        if user_channel_status["status"] != 'left' and user_channel_status["status"] != 'kicked':
            data1[str(channels[channel])] = str(user_channel_status['user']['id'])
        user = await bot.get_chat_member(chat_id=channels[channel], user_id=message.from_user.id)
        if user.status == "member" or user.status == "creator" or user.status == "administrator":
            counter += 1
    if counter != 0:
        await FSMClientClean.yes_no.set()
        await bot.send_message(message.from_user.id, 'Уборка закончена?', reply_markup=clean1)
    else:
        await bot.send_message(message.from_user.id, 'Вы не являетесь администратором',
                               reply_markup=ReplyKeyboardRemove())


async def get_clean_yes_no(message: types.Message, state: FSMContext):
    if message.chat.id == config.chat_id_zel and message.from_user.id != config.bot_id:
        await message.delete()
        return
    else:
        async with state.proxy() as data_clean:
            data_clean['yes_no'] = message.text
            if data_clean['yes_no'] == 'Да':
                await FSMClientClean.next()
                await bot.send_message(message.from_user.id,
                                       'Уборка туалетов была произведена качественно (запах, пол, зеркала, унитаз,'
                                       ' стены)? Оцените от 1 до 5',
                                       reply_markup=back_button_admin)

            elif data_clean['yes_no'] == 'Нет':
                await bot.send_message(message.from_user.id, 'Дождитесь окончания уборки. Я напишу вам через 15 минут',
                                       reply_markup=back_button)
                await asyncio.sleep(900)
                await FSMClientClean.yes_no.set()
                await bot.send_message(message.from_user.id, 'Уборка закончена?', reply_markup=clean1)
            else:
                await bot.send_message(message.from_user.id, 'Такой ответ не предусмотрен')
                await FSMClientClean.yes_no.set()
                await bot.send_message(message.from_user.id, 'Уборка закончена?', reply_markup=clean1)


async def get_clean_toilets(message: types.Message, state: FSMContext):
    global current_state
    current_state = await state.get_state()
    if message.chat.id == config.chat_id_zel and message.from_user.id != config.bot_id:
        await message.delete()
        return
    if message.text == "Назад":
        await FSMClientClean.yes_no.set()
        await bot.send_message(message.from_user.id, 'Уборка закончена?', reply_markup=clean1)
    else:
        async with state.proxy() as data_clean:
            data_clean['toilets'] = message.text
        if int(data_clean['toilets']) == 5:
            await FSMClientClean.next()
            await bot.send_message(message.from_user.id,
                                   'Уборка помещения (этажи, лестница, полы во всем помещении)? Оцените от 1 до 5',
                                   reply_markup=back_button_admin)
        elif int(data_clean['toilets']) < 5:
            await bot.send_message(message.from_user.id, 'Почему такая оценка? Укажите причину',
                                   reply_markup=back_button_admin)
            await FSMClientClean.reason.set()
        else:
            pass


async def get_clean_rooms(message: types.Message, state: FSMContext):
    global current_state
    current_state = await state.get_state()
    if message.chat.id == config.chat_id_zel and message.from_user.id != config.bot_id:
        await message.delete()
        return
    if message.text == "Назад":
        await FSMClientClean.toilets.set()
        await bot.send_message(message.from_user.id,
                               'Уборка туалетов была произведена качественно (запах, пол, зеркала, унитаз, стены)?'
                               ' Оцените от 1 до 5',
                               reply_markup=back_button_admin)
    else:
        async with state.proxy() as data_clean:
            data_clean['rooms'] = message.text
        if int(data_clean['rooms']) == 5:
            await FSMClientClean.next()
            await bot.send_message(message.from_user.id,
                                   'Уборка периферии (столы, мониторы, клавиатуры, мышки, коврики)? Оцените от 1 до 5',
                                   reply_markup=back_button_admin)
        elif int(data_clean['rooms']) < 5:
            await bot.send_message(message.from_user.id, 'Почему такая оценка? Укажите причину',
                                   reply_markup=back_button_admin)
            await FSMClientClean.reason.set()
        else:
            pass


async def get_clean_tables(message: types.Message, state: FSMContext):
    global current_state
    current_state = await state.get_state()
    if message.chat.id == config.chat_id_zel and message.from_user.id != config.bot_id:
        await message.delete()
        return
    if message.text == "Назад":
        await FSMClientClean.rooms.set()
        await bot.send_message(message.from_user.id,
                               'Уборка помещения (этажи, лестница, полы во всем помещении)? Оцените от 1 до 5',
                               reply_markup=back_button_admin)
    else:
        async with state.proxy() as data_clean:
            data_clean['tables'] = message.text
        if int(data_clean['tables']) == 5:
            result = 'Отчет по уборке:\n'
            for key in data_clean:
                if key == 'toilets':
                    result += f'Уборка туалетов (запах, пол, зеркала, унитаз, стены): {data_clean["toilets"]}\n'
                if key == 'fanc0':
                    result += f'Причина оценки: {data_clean["fanc0"]}\n'
                if key == 'rooms':
                    result += f'Уборка помещения (этажи, лестница, полы во всем помещении): {data_clean["rooms"]}\n'
                if key == 'fanc1':
                    result += f'Причина оценки: {data_clean["fanc1"]}\n'
                if key == 'tables':
                    result += f'Уборка периферии (столы, мониторы, клавиатуры, мышки, коврики): {data_clean["tables"]}\n'
                if key == 'fanc2':
                    result += f'Причина оценки: {data_clean["fanc2"]}\n'
            await bot.send_message(message.from_user.id, 'Спасибо за отчет. Хорошей вам смены!',
                                   reply_markup=kb_client1)
            await bot.send_message(chat_id=chat_id_zel,
                                   text=result)
            await state.finish()
        elif int(data_clean['tables']) < 5:
            await bot.send_message(message.from_user.id, 'Почему такая оценка? Укажите причину',
                                   reply_markup=back_button_admin)
            await FSMClientClean.reason.set()
        else:
            pass


count = 0


async def get_clean_reason(message: types.Message, state: FSMContext):
    global current_state
    global count
    if message.text == "Назад":
        if current_state == 'FSMClientClean:toilets':
            await FSMClientClean.toilets.set()
            await bot.send_message(message.from_user.id,
                                   'Уборка туалетов была произведена качественно (запах, пол, зеркала, унитаз, стены)?'
                                   ' Оцените от 1 до 5',
                                   reply_markup=back_button_admin)
        elif current_state == 'FSMClientClean:rooms':
            await FSMClientClean.rooms.set()
            await bot.send_message(message.from_user.id,
                                   'Уборка помещения (этажи, лестница, полы во всем помещении)? Оцените от 1 до 5',
                                   reply_markup=back_button_admin)
        elif current_state == 'FSMClientClean:tables':
            await FSMClientClean.tables.set()
            await bot.send_message(message.from_user.id,
                                   'Уборка периферии (столы, мониторы, клавиатуры, мышки, коврики)? Оцените от 1 до 5',
                                   reply_markup=back_button_admin)
    else:
        async with state.proxy() as data_clean:
            data_clean[f'fanc{count}'] = message.text
        print(data_clean)
        result = 'Отчет по уборке:\n'
        for key in data_clean:
            if key == 'toilets':
                result += f'Уборка туалетов (запах, пол, зеркала, унитаз, стены): {data_clean["toilets"]}\n'
            if key == 'fanc0':
                result += f'Причина оценки: {data_clean["fanc0"]}\n'
            if key == 'rooms':
                result += f'Уборка помещения (этажи, лестница, полы во всем помещении): {data_clean["rooms"]}\n'
            if key == 'fanc1':
                result += f'Причина оценки: {data_clean["fanc1"]}\n'
            if key == 'tables':
                result += f'Уборка периферии (столы, мониторы, клавиатуры, мышки, коврики): {data_clean["tables"]}\n'
            if key == 'fanc2':
                result += f'Причина оценки: {data_clean["fanc2"]}\n'
        if current_state == 'FSMClientClean:toilets':
            await FSMClientClean.rooms.set()
            await bot.send_message(message.from_user.id,
                                   'Уборка помещения (этажи, лестница, полы во всем помещении)? Оцените от 1 до 5',
                                   reply_markup=back_button_admin)
        elif current_state == 'FSMClientClean:rooms':
            await FSMClientClean.tables.set()
            await bot.send_message(message.from_user.id,
                                   'Уборка периферии (столы, мониторы, клавиатуры, мышки, коврики)? Оцените от 1 до 5',
                                   reply_markup=back_button_admin)
        elif current_state == 'FSMClientClean:tables':
            await bot.send_message(message.from_user.id, 'Спасибо за отчет. Хорошей вам смены!',
                                   reply_markup=kb_client1)
            await bot.send_message(chat_id=chat_id_zel,
                                   text=result)
            await state.finish()
        count += 1


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(day_night, text=['Дневная смена', 'Ночная смена'])
    dp.register_message_handler(cancel_handler, Text(equals='Вернуться в начальное меню', ignore_case=True), state="*")
    dp.register_message_handler(q1, state=FSMClient.q1)
    dp.register_message_handler(q2, state=FSMClient.q2)
    dp.register_message_handler(q3, state=FSMClient.q3)
    dp.register_message_handler(q4, state=FSMClient.q4)
    dp.register_message_handler(q5, state=FSMClient.q5)
    dp.register_message_handler(q6, state=FSMClient.q6)
    dp.register_message_handler(q7, state=FSMClient.q7)
    dp.register_message_handler(q8, state=FSMClient.q8)
    dp.register_message_handler(q9, state=FSMClient.q9)
    dp.register_message_handler(q10, state=FSMClient.q10)
    dp.register_message_handler(q11, state=FSMClient.q11)
    dp.register_message_handler(q12, state=FSMClient.q12)
    dp.register_message_handler(q13, state=FSMClient.q13)
    dp.register_message_handler(q14, state=FSMClient.q14)
    dp.register_message_handler(q15, state=FSMClient.q15)
    dp.register_message_handler(q16, state=FSMClient.q16)
    dp.register_message_handler(q17, state=FSMClient.q17)
    dp.register_message_handler(q18, state=FSMClient.q18)
    dp.register_message_handler(get_nonfunctioning_equipment, state=FSMClient.get_nonfunc_equipment)
    dp.register_message_handler(late, text=['Задерживаюсь на смену'])
    dp.register_message_handler(get_late1, state=FSMClientLate.q1)
    dp.register_message_handler(get_late2, state=FSMClientLate.q2)
    dp.register_message_handler(clean, text=['Отчет по уборке'])
    dp.register_message_handler(get_clean_yes_no, state=FSMClientClean.yes_no)
    dp.register_message_handler(get_clean_toilets, state=FSMClientClean.toilets)
    dp.register_message_handler(get_clean_rooms, state=FSMClientClean.rooms)
    dp.register_message_handler(get_clean_tables, state=FSMClientClean.tables)
    dp.register_message_handler(get_clean_reason, state=FSMClientClean.reason)
    dp.register_message_handler(cancel_handler, state="*", commands='Вернуться в начальное меню')
