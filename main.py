from keyboards import kb, ikb_link, ikb_vote
from aiogram import Bot, Dispatcher, executor, types

from config import (
    API_TOKEN, sticker_id, sticker_id2,
    photo_link, girl_photo_id, HELP_COMMAND
)

bot = Bot(token=API_TOKEN)
db = Dispatcher(bot)


async def start_up(_):
    print("Bot working...")


@db.message_handler(commands=['phone_number'])
async def share_phone_number(message: types.Message):
    await message.reply(
        text="share phone number", reply_markup=kb
    )


@db.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        parse_mode='HTML',
        text=HELP_COMMAND,
        reply_markup=kb
    )


@db.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        reply_markup=kb,
        text='Salom !',
        parse_mode='HTML'
    )


@db.message_handler(commands=['links'])
async def send_link(message: types.Message):
    await message.answer(
        text='select options...',
        reply_markup=ikb_link
    )


@db.message_handler(commands=['give'])
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


@db.message_handler(commands=['photo'])
async def send_photo(message: types.Message):
    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=photo_link, reply_markup=kb
    )


@db.message_handler(commands=['office'])
async def office_location(message: types.Message):
    await bot.send_location(
        message.from_user.id,
        latitude=41.302899,
        longitude=69.314737,
        reply_markup=kb
    )


@db.message_handler(commands=['home'])
async def home_location(message: types.Message):
    await bot.send_location(
        message.from_user.id,
        latitude=41.380281,
        longitude=69.131573,
        reply_markup=kb
    )


@db.message_handler(commands=['vote'])
async def vote_command(message: types.Message):
    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=girl_photo_id,
        caption='do you like that girl?',
        reply_markup=ikb_vote
    )


@db.callback_query_handler()
async def vote_callback(callback: types.CallbackQuery):
    if callback.data == 'like':
        await callback.answer(text='Sizga yoqqandan hursandman 😊')
    await callback.answer(text="Sizga boshqa varyantlarni ko'rsataman")

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
