import requests
import re

from image_service import image_downloader
from aiogram import Bot, Dispatcher, executor, types
from db.repositories import message_repository, message_metadata_repository, link_repository

consult_bot_api_token = '2140772750:AAHQCi_kfi10zTCHDFs1bghEpeLJhQP7CRI'

bot = Bot(token=consult_bot_api_token)
dp = Dispatcher(bot)


@dp.message_handler()
async def send_welcome(message: types.Message):
    await message.answer('Hello! I\'m here')
    await message_repository.create(message.text)

    find_url_regex = re.search("(?P<url>https?://[^\s]+)", message.text)

    if find_url_regex is not None:
        url = find_url_regex.group(0)
        response = requests.get(url)
        pat = re.compile(r'<img [^>]*src="([^"]+)')
        images = pat.findall(response.text)
        images = images[:10]
        if images:
            is_nsfw = await image_downloader.is_nsfw(images)

            if is_nsfw:
                await message.delete()

            # await message.answer('Your message is on moderating')

        await message.answer('Didn\'t find images')
    else:
        await message.answer('Ok')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
