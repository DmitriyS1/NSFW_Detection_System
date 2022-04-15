from aiogram.types.message import ContentType
from aiogram.types.user_profile_photos import UserProfilePhotos
import logging
import requests
import re

from image_service import image_downloader
from aiogram.bot import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram import types
from aiogram.types import Message as TgMessage
from db.repositories import message_repository, message_metadata_repository, link_repository, group_repository, admin_repository, temp_admin_repository

# bot_token = '2140772750:AAHQCi_kfi10zTCHDFs1bghEpeLJhQP7CRI'  # Consulting4d (test bot)
bot_token = '5035659135:AAGGzpwziuAA1IQACwIMp32zbBQ943cbXjc'  # Production Bot
bot = Bot(token=bot_token)
dp = Dispatcher(bot)

logger = logging.getLogger(__name__)

@dp.message_handler(commands=["start"])
async def add_new_admin(message: types.Message):
    members_count = await message.chat.get_members_count() # проверить, что пользователь в личном чате, а не в группе. А в обработчике activate проверять, что вызов в группе. Может ли в группе быть меньше 2 пользователей
    if members_count > 2:
        return # log info about chat and user

    new_admin_id = message.from_user.id
    personal_chat_id = message.chat.id
    existed_temp_admin = temp_admin_repository.get(new_admin_id)
    if existed_temp_admin:
        existed_admin = admin_repository.get(new_admin_id)
        if not existed_admin:
            existed_admin = admin_repository.create(existed_temp_admin.id, existed_temp_admin.name, personal_chat_id)
        
        chat = group_repository.update(existed_temp_admin.chat_id, existed_admin.id, True)

        await bot.send_message(message.chat.id, text=f"Вы успешно зарегистрировали чат {chat.name}. Защита от спама активна.")
        return
    else:
        await bot.send_message(message.chat.id, text=f"Видимо чат еще не обнаружен ботом. Если вы уже добавили бота в ваш чат, попробуйте снова вызвать /start через 10 минут")
        return



@dp.message_handler(content_types=ContentType.PHOTO)
async def moderate_photo(message: types.Message):
    #moderate any photo or list of photos
    return

@dp.message_handler()
async def moderate_msg(message: types.Message):
    group = group_repository.get(message.chat.id)
    if not group:
        admins = await message.chat.get_administrators()
        for admin in admins:
            temp_admin_repository.create(admin.user.id, f"{admin.user.first_name} {admin.user.last_name}", message.chat.id)
        
        group_repository.create(message.chat.id, None, message.chat.full_name)
        return
    elif not group.is_moderation_active:
        return
    

    is_admin = await is_sent_by_admin(message)
    if not is_admin and (message.from_user.first_name == "Channel" or message.from_user.full_name == "Channel"):
        await bot.delete_message(message.chat.id, message.message_id)
        return

    find_url_regex = re.search("(?P<url>https?://[^\s]+)", message.text)

    if find_url_regex is not None:
        url = find_url_regex.group(0)
        existed_link = link_repository.get(link=url)
        if existed_link is not None:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            return

        images_links = get_image_links(url)

        if images_links:
            is_nsfw = await image_downloader.is_nsfw(images_links)
            if is_nsfw:
                await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                save_info_to_db(message, url, False)
                return

    avatars = await bot.get_user_profile_photos(user_id=message.from_user.id)
    photo_urls = await make_avatar_links(avatars, bot)
    if photo_urls:
        is_nsfw, url = await image_downloader.is_nsfw(photo_urls)
        if is_nsfw:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            save_info_to_db(message, url=url, is_blocked_by_avatar=True)


def get_image_links(resource_url: str):
    """
    Return type - list(str)
    """

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


async def make_avatar_links(avatars: UserProfilePhotos, bot: Bot):
    """
    Return type - list(str)
    """
    
    urls = []
    avatars_count = 2
    if len(avatars.photos[0]) > avatars_count:
        user_photos = avatars.photos[0][:avatars_count]
    else:
        user_photos = avatars.photos[0]

    for photo in user_photos:
        file = await bot.get_file(file_id=photo.file_id)
        urls.append(f"https://api.telegram.org/file/bot{bot_token}/{file.file_path}")
        
    return urls


def save_info_to_db(message: TgMessage, url: str, is_blocked_by_avatar: bool):
    msg = message_repository.create(message.text, is_blocked_by_avatar)
    msg_metadata = message_metadata_repository.create(
        chat_id=message.chat.id, msg_id=msg.id, tg_msg_id=message.message_id, user_id=message.from_user.id)
    link_repository.create(msg_metadata.id, url)


async def is_sent_by_admin(message: TgMessage) -> bool:
    admins = await message.chat.get_administrators()
    result = False
    for admin in admins:
        if admin.user.id == message.from_user.id:
            result = True
    
    return result



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
