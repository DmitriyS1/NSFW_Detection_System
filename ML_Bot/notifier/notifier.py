from io import BytesIO
from aiogram import Bot
from aiogram.types import InputFile
from aiogram.types.message import ParseMode
from aiogram.utils import markdown
from sqlalchemy.sql.sqltypes import Integer
from db.repositories import resume_repository, user_repository

CHANNEL_ID = -1001446793857

async def send_registration_notification(bot: Bot, user_id: int):
    user = user_repository.get(user_id)
    if user is None:
        return
    
    msg = markdown.text(
        markdown.bold("Username: "),
        user.username,
        markdown.bold("\nИмя: "),
        user.first_name,
        markdown.bold("\nФамилия: "),
        user.last_name,
        markdown.bold("\nДата регистрации: "),
        user.created_at)

    resume = resume_repository.get_by_user_id(user_id)
    file = BytesIO(resume.file_data)
    buf_file = InputFile(file, filename=resume.filename)

    await bot.send_document(chat_id=CHANNEL_ID, document=buf_file, caption=msg, parse_mode=ParseMode.MARKDOWN)

async def send_question_from_user(bot: Bot, message_id: Integer, from_chat_id: Integer):
    await bot.forward_message(chat_id=CHANNEL_ID, from_chat_id=from_chat_id, message_id=message_id)

async def send_yesterday_count_notification(bot: Bot):
    # Опросить бд на предмет зарегистрированных вчера
    # Настроить отправку каждое утро
    await bot.send_message(chat_id=CHANNEL_ID, text="Hello")

