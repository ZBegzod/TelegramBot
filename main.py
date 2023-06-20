import random
from aiogram.dispatcher.filters import Text
from config import (
    API_TOKEN, sticker_id, sticker_id2,
    photo_1, photo_2, photo_3, photo_4, photo_5, HELP_COMMAND
)
from aiogram.types import (
    ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
)
from keyboards import (
    kb, ikb_photo, ikb_link
)
from aiogram import (
    Bot, Dispatcher, executor, types
)

flag = False
number = 0
bot = Bot(token=API_TOKEN)
db = Dispatcher(bot)

array_photo = [photo_1, photo_2, photo_3, photo_4, photo_5]
photos = dict(zip(array_photo, ['1', '2', '3', '4', '5']))
random_photo_v = random.choice(list(photos.keys()))


async def start_up(_):
    print("Bot working...")


async def send_random(message: types.Message):
    global random_photo_v
    random_photo_v = random.choice(list(photos.keys()))

    await bot.send_photo(
        chat_id=message.chat.id,
        photo=random_photo_v,
        caption=photos[random_photo_v],
        reply_markup=ikb_photo
    )


@db.message_handler(Text(equals='random photo'))
async def random_photo(message: types.Message):
    await send_random(message=message)


@db.callback_query_handler(
    lambda callback_query:
    callback_query.data == 'like' or
    callback_query.data == 'dislike' or
    callback_query.data == 'main' or
    callback_query.data == 'next'
)
async def callback_query_photo(callback: types.CallbackQuery):
    print(callback)
    global random_photo_v, flag
    if callback.data == 'like':
        if not flag:
            await callback.answer('you reacted like!')
            flag = not flag
        else:
            await callback.answer('you already reacted like!')
    elif callback.data == 'dislike':
        await callback.answer('you reacted dislike!')
    elif callback.data == 'main':
        await callback.message.answer('Welcome to main section', reply_markup=kb)
        await callback.message.delete()
    else:
        random_photo_v = random.choice(list(filter(lambda x: x != random_photo_v, list(photos.keys()))))
        await callback.message.edit_media(types.InputMedia(
            type='photo',
            media=random_photo_v,
            caption=photos[random_photo_v]),
            reply_markup=ikb_photo)


def get_inline_keyboard() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton('Increase', callback_data='btn_increase'),
            InlineKeyboardButton('Decrease', callback_data='btn_decrease')
        ]
    ])
    return ikb


@db.callback_query_handler(lambda callback_query: callback_query.data.startswith('btn'))
async def callback_increase_decrease(callback: types.CallbackQuery):
    global number
    if callback.data == 'btn_decrease':
        number += 1
        await callback.message.edit_text(
            text=f"The current number is {number}",
            reply_markup=get_inline_keyboard()
        )
    elif callback.data == 'btn_increase':
        number -= 1
        await callback.message.edit_text(
            text=f"The current number is {number}",
            reply_markup=get_inline_keyboard()
        )
    else:
        1 / 0


@db.message_handler(commands=['phone_number'])
async def share_phone_number(message: types.Message):
    await message.reply(
        text="share phone number", reply_markup=kb
    )


@db.message_handler(Text(equals='help'))
async def help_command(message: types.Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        parse_mode='HTML',
        text=HELP_COMMAND,
        reply_markup=kb
    )


@db.message_handler(Text(equals='start'))
async def send_welcome(message: types.Message):
    await message.answer(
        text=f'The current number is {number}',
        reply_markup=get_inline_keyboard()
    )


@db.message_handler(Text(equals='links'))
async def send_link(message: types.Message):
    await message.answer(
        text='select options...',
        reply_markup=ikb_link
    )


@db.message_handler(Text(equals='give'))
async def give_sticker(message: types.Message):
    await bot.send_sticker(
        message.from_user.id,
        sticker=sticker_id,
        reply_markup=kb
    )


@db.message_handler(content_types=['sticker'])
async def send_sticker(message: types.Message):
    await message.answer(
        message.sticker.file_id,
        reply_markup=kb
    )


@db.message_handler(content_types=['location'])
async def get_location(message: types.Message):
    lat = message.location.latitude
    lot = message.location.longitude
    reply = "latitude: {}\n longitude: {}".format(lat, lot)
    await message.answer(reply, reply_markup=kb)


@db.message_handler(Text(equals='photo'))
async def send_photo(message: types.Message):
    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=photo_1, reply_markup=kb
    )


@db.message_handler(Text(equals='office'))
async def office_location(message: types.Message):
    await bot.send_location(
        message.from_user.id,
        latitude=41.302899,
        longitude=69.314737,
        reply_markup=kb
    )


@db.message_handler(Text(equals='home'))
async def home_location(message: types.Message):
    await bot.send_location(
        message.from_user.id,
        latitude=41.380281,
        longitude=69.131573,
        reply_markup=kb
    )


# @db.message_handler(Text(equals='vote'))
# async def vote_command(message: types.Message):
#     await bot.send_photo(
#         chat_id=message.from_user.id,
#         photo=girl_photo_id,
#         caption='do you like that girl?',
#         reply_markup=ikb_vote
#     )


# @db.callback_query_handler()
# async def vote_callback(callback: types.CallbackQuery):
#     if callback.data == 'like':
#         await callback.answer(text='you reacted like !')
#     await callback.answer(text="you reacted dislike !")


# @db.message_handler()
# async def send_random_letter(message: types.Message):
#     await message.reply(string.ascii_letters)


# @db.message_handler()
# async def echo(message: types.Message):
#     await message.answer(message.text.upper())

# @db.message_handler()
# async def send_love(message: types.Message):
#     if message.text == '❤':
#         await bot.send_sticker(
#             chat_id=message.from_user.id,
#             sticker=sticker_id2
#         )
#

if __name__ == '__main__':
    executor.start_polling(
        dispatcher=db,
        skip_updates=True,
        on_startup=start_up
    )
