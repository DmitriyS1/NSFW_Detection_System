from aiogram.types.message import ContentType
from aiogram.types.user_profile_photos import UserProfilePhotos
import requests
import re

from image_service import image_downloader
from aiogram.bot import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram import types
from aiogram.types import Message as TgMessage
from db.repositories import message_repository, message_metadata_repository, link_repository, group_repository, admin_repository

bot_token = '2140772750:AAHQCi_kfi10zTCHDFs1bghEpeLJhQP7CRI'  # Consulting4d (test bot)
# bot_token = '5035659135:AAGGzpwziuAA1IQACwIMp32zbBQ943cbXjc'  # Production Bot
bot = Bot(token=bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def add_new_admin(message: types.Message):
    members_count = await message.chat.get_members_count() # проверить, что пользователь в личном чате, а не в группе. А в обработчике activate проверять, что вызов в группе. Может ли в группе быть меньше 2 пользователей
    if members_count > 2:
        return # log info about chat and user
    new_admin_id = message.from_user.id
    existed_admin = admin_repository.get(new_admin_id)
    if existed_admin:
        await bot.send_message(message.chat.id, text="У вас уже есть модерируемые чаты.\n Нажмите /help для дополнительных инструкций")
        return
    
    admin_repository.create(message.from_user.id, message.from_user.full_name, message.chat.id)
    await bot.send_message(message.chat.id, text="Добро пожаловать!\nДобавте бота в чат, сделав администратором. Затем выполните команду /activate в вашем чате. Дальше все случится автоматически.\nНаслаждайтесь чистым чатом")


@dp.message_handler(commands=["activate"])
async def activate_chat(message: types.Message):
    new_chat_id = message.chat.id
    admins = await message.chat.get_administrators()
    existed_chat = group_repository.get(new_chat_id)
    if not existed_chat:
        return

    registered_admin = admin_repository.get(message.from_user.id)
    if registered_admin is None:
        return

    match = (admin for admin in admins if admin.user.id == registered_admin.id)
    if match:
        # add admin to chat or smth
        return


@dp.message_handler(content_types=ContentType.PHOTO)
async def moderate_photo(message: types.Message):
    #moderate any photo or list of photos
    return

@dp.message_handler()
async def moderate_msg(message: types.Message):
    is_admin = await is_sent_by_admin(message)
    if not is_admin and (message.from_user.first_name == "Channel" or message.from_user.full_name == "Channel" or message.from_user.mention == "@Channel_Bot"):
        await bot.delete_message(message.chat.id, message.message_id)

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
