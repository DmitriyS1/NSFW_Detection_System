from datetime import datetime, timezone
from io import BytesIO

import requests
import json
import re

from image_service import image_downloader

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType

from pathlib import Path
from bot_messages import BotMessages

consult_bot_api_token = '2140772750:AAHQCi_kfi10zTCHDFs1bghEpeLJhQP7CRI'

bot = Bot(token=consult_bot_api_token)
dp = Dispatcher(bot)

@dp.message_handler()
async def send_welcome(message: types.Message):
        find_url_regex = re.search("(?P<url>https?://[^\s]+)", message.text)
        if find_url_regex is not None:
                url = find_url_regex.group(0)
                response = requests.get(url)
                pat = re.compile(r'<img [^>]*src="([^"]+)')
                images = pat.findall(response.text)
                images = images[:10]
                if images:
                        for i in range(len(images)):
                                if "http" not in images[i] or ".svg" in images[i]:
                                        images[i] = ''
                        
                        #здесь сохранить в бд и отправлять дальше по конвееру
                        images = list(filter(None, images))
                        is_nsfw = await image_downloader.is_nsfw(images)
                        
                        if is_nsfw:
                                await bot.delete_message(message.chat.id, message.message_id)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
