import requests
import re

from image_service import image_downloader
from aiogram.bot import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram import types
from db.repositories import message_repository, message_metadata_repository, link_repository

# bot_token = '2140772750:AAHQCi_kfi10zTCHDFs1bghEpeLJhQP7CRI'  # Consulting4d (test bot)
bot_token = '5035659135:AAGGzpwziuAA1IQACwIMp32zbBQ943cbXjc'  # Production Bot
bot = Bot(token=bot_token)
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

        images_links = get_image_links(url)
        # get_avatars(photos: UserProfilePhotos)

        if images_links:
            is_nsfw = await image_downloader.is_nsfw(images_links)

            if is_nsfw:
                await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                msg = message_repository.create(message.text)
                msg_metadata = message_metadata_repository.create(
                    chat_id=message.chat.id, msg_id=msg.id, tg_msg_id=message.message_id, user_id=message.from_user.id)
                link_repository.create(msg_metadata.id, url)


def get_image_links(resource_url: str) -> list(str):
    response = requests.get(resource_url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    })

    pat = re.compile(
        r'[\=,\(][\"|\'].[^\=\"]+\.(?i:jpg|jpeg|png|bmp)[\"|\']')
    images_links = pat.findall(response.text)
    imageLinksFilter = filter(lambda url: 'icon' not in url, images_links)
    images_links = list(imageLinksFilter)
    images_links = images_links[:10]
    for i, image in enumerate(images_links):
        images_links[i] = image.replace('=', '').replace('"', '')

    return images_links


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
