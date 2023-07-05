import os
import datetime
from pytube import YouTube
from config import API_TOKEN

from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def load_vidio(message: types.Message):
    if message.text.startswith('https://youtube.be/') or message.text.startswith(
            'https://www.youtube.com/') or message.text.startswith('https://youtu.be/'):

        url = message.text
        yt = YouTube(url)
        yt.check_availability()

        title = yt.title
        author = yt.author

        length = yt.length
        views = yt.views

        channel = yt.channel_url
        picture = yt.thumbnail_url

        # date_published = yt.publish_date.strftime('%Y-%m-%d')
        resolution = yt.streams.get_highest_resolution().resolution
        file_size = yt.streams.get_highest_resolution().filesize

        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text='click', callback_data='download'))

        await message.answer_photo(
            f"{picture}", caption=f"📹<b>{title}</b> <a href='{url}'>→</a> \n"  # title
                                  f"👤<b>{author}</b> <a href='{channel}'>→</a> \n"  # Author of channel
                                  f"⚙<b>Expansion-</b> <code>{resolution}</code> \n"  # expansion'
                                  f"<b>Video important-</b> <code>{round(file_size * 0.000001, 2)}</code> \n"
                                  f"<b>Trivality-</b> <code>{str(datetime.timedelta(seconds=length))}</code> \n"
                                  # f"🗓 <b>Published date—</b> <code>{date_published}</code> \n"  # Date Published#
                                  f"👁 <b>Перегляди —</b> <code>{views:,}</code> \n",
            parse_mode='HTML', reply_markup=keyboard)  # Views

    else:
        await message.answer(f"❗<b>invalid link !</b>", parse_mode='HTML')


@dp.callback_query_handler(text='download')
async def button_download(call: types.CallbackQuery):
    url = call.message.html_text
    yt = YouTube(url=url)
    yt.check_availability()

    title = yt.title
    author = yt.author

    resolution = yt.streams.get_highest_resolution().resolution
    stream = yt.streams.filter(progressive=True, file_extension='mp4')
    stream.get_highest_resolution().download(filename='video.mp4')

    with open("video.mp4", 'rb') as video:
        await bot.send_video(
            call.message.chat.id, video,
            caption=f"📹 <b>{title}</b> \n"  # Title
                    f"👤<b>{author}</b> \n\n"  # Author Of Channel
                    f"⚙<b>Expansion —</b> <code>{resolution}</code> \n"
                    f"📥<b>Interested in help @Helper_YouTube_Bot</b>", parse_mode='HTML'
        )
        os.remove("video.mp4")


if __name__ == '__main__':
    executor.start_polling(
        dispatcher=dp,
        skip_updates=True
    )
