from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


q11 = KeyboardButton('Дневная смена')
q12 = KeyboardButton('Ночная смена')
q13 = KeyboardButton('Задерживаюсь на смену')
q21 = KeyboardButton('Да')
q22 = KeyboardButton('Нет')
q31 = KeyboardButton('Компьютер')
q32 = KeyboardButton('Телефон')
q4 = KeyboardButton('Отчет по уборке')

client_out = KeyboardButton('Вернуться в начальное меню')
client_out_button = ReplyKeyboardMarkup(resize_keyboard=True)
client_out_button.add(client_out)

b4 = KeyboardButton('Поделиться расположением', request_location=True)
kb_client_location = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client_location.add(b4)

back = KeyboardButton('Назад')
back_button = ReplyKeyboardMarkup(resize_keyboard=True)
back_button.add(back).insert(client_out)

back_button_admin = ReplyKeyboardMarkup(resize_keyboard=True)
back_button_admin.add(back)

next_b = KeyboardButton('Далее')
next_button = ReplyKeyboardMarkup(resize_keyboard=True)
next_button.add(back).insert(next_b)

clean1 = ReplyKeyboardMarkup(resize_keyboard=True)
clean1.add(q21).insert(q22).add(client_out)

fine = KeyboardButton('Выписать штраф')
fine_button = ReplyKeyboardMarkup(resize_keyboard=True)
fine_button.add(fine)

zel = KeyboardButton('Зеленогорск')
spb = KeyboardButton('Санкт-Петербург')
ekb = KeyboardButton('Екатеринбург')
nsk = KeyboardButton('Новосибирск')
krsku = KeyboardButton('Красноярск (Урванцева)')
krskk = KeyboardButton('Красноярск (Качинская)')
clubs = ReplyKeyboardMarkup(resize_keyboard=True)
clubs.add(zel).insert(spb).add(ekb).insert(nsk).add(krsku).insert(krskk).add(back)

general = KeyboardButton('Отправить в общий чат')
confidential = KeyboardButton('Отправить конфиденциально')
decision = ReplyKeyboardMarkup(resize_keyboard=True)
decision.add(general).insert(confidential).add(back)

kb_client1 = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client2 = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client3 = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client4 = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client1.add(q11).insert(q12).add(q13).insert(q4)
kb_client2.add(q21).insert(q22).add(back).insert(client_out)
kb_client3.add(q31).insert(q32).add(back).insert(client_out)
kb_client4.add(q11).insert(q12).add(q13).insert(q4).add(fine)
