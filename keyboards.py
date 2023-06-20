from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardButton, InlineKeyboardMarkup
)

kb = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
)

b1 = KeyboardButton('help')
b2 = KeyboardButton('start')

b3 = KeyboardButton('photo')
b4 = KeyboardButton('give')

b5 = KeyboardButton('links')
b6 = KeyboardButton('vote')

b7 = KeyboardButton('office')
b8 = KeyboardButton('home')

b9 = KeyboardButton('phone number', request_contact=True)
b10 = KeyboardButton('random photo')

kb = kb.add(b1).insert(b2).insert(b3).add(b4).insert(b5)
kb.insert(b6).insert(b7).insert(b8).insert(b9).insert(b10)

ikb_link = InlineKeyboardMarkup(
    row_width=2
)

ib1 = InlineKeyboardButton(
    text='YouTube', url='https://www.youtube.com/'
)

ib2 = InlineKeyboardButton(
    text='Google', url='https://www.google.com/'
)

ikb_link.add(ib1, ib2)

ikb_photo = InlineKeyboardMarkup(
    row_width=2
)

ibp1 = InlineKeyboardButton(
    text='👍', callback_data='like'
)
ibp2 = InlineKeyboardButton(
    text='👎', callback_data='dislike'
)
ibp3 = InlineKeyboardButton(
    text='random another photo',
    callback_data='next'
)
ibp4 = InlineKeyboardButton(
    text='main section',
    callback_data='main'
)

ikb_photo.add(ibp1, ibp2).add(ibp3).add(ibp4)
