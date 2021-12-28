import requests
import re

from image_service import image_downloader
from aiogram.bot import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram import types
from db.repositories import message_repository, message_metadata_repository, link_repository

consult_bot_api_token = '2140772750:AAHQCi_kfi10zTCHDFs1bghEpeLJhQP7CRI'

bot = Bot(token=consult_bot_api_token)
dp = Dispatcher(bot)


@dp.message_handler()
async def send_welcome(message: types.Message):
    find_url_regex = re.search("(?P<url>https?://[^\s]+)", message.text)

    if find_url_regex is not None:
        url = find_url_regex.group(0)
        existed_link = link_repository.get(link=url)
        if existed_link is not None:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            return

        response = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        })

        pat = re.compile(
            r'[\=,\(][\"|\'].[^\=\"]+\.(?i:jpg|jpeg|png|bmp)[\"|\']')
        images = pat.findall(response.text)
        images = images[:10]
        for i, image in enumerate(images):
            images[i] = image.replace('=', '').replace('"', '')

        if images:
            is_nsfw = await image_downloader.is_nsfw(images)

            if is_nsfw:
                await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                msg = message_repository.create(message.text)
                msg_metadata = message_metadata_repository.create(
                    chat_id=message.chat.id, msg_id=msg.id, tg_msg_id=message.message_id, user_id=message.from_user.id)
                link_repository.create(msg_metadata.id, url)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
