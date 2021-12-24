from datetime import datetime, timezone
from io import BytesIO

import requests
import json
import re

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
                
                if images:
                        #здесь сохранить в бд и отправлять дальше по конвееру
                        await message.answer('Your message is on moderating')

                await message.answer('Didn\'t find images')
        else:
                await message.answer('Ok')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
