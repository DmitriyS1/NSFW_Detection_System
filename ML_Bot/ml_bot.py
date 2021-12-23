from datetime import datetime, timezone
from io import BytesIO

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType

from pathlib import Path
from bot_messages import BotMessages
from notifier import notifier


API_TOKEN = '618909382:AAEMG0jXMgDTGm6eCxwCwzFFUWZ9RodyVdM' # 4d_test
#API_TOKEN = '1885273122:AAHSUzWGpu5OCB2C9WXcEwFF8RCt87AnIaw' # first_job
# print("Token from config: ", config['bot_token'])

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user = user_repository.get(message.from_user.id)
    if user is None:
        user = set_user_from_message(message)
        user_repository.create(user)
        await bot.send_message(message.chat.id, text=BotMessages['start_new'])
    else:
        await bot.send_message(message.chat.id, text=BotMessages['start_existed'])


@dp.message_handler(content_types=ContentType.DOCUMENT)
async def save_resume(message: types.Message):
    file_name = Path(message.document.file_name)
    if not is_resume_extension_valid(file_name.suffix):
        await bot.send_message(message.chat.id, text=BotMessages['file_upload_ext_error'].format(file_name.suffix))
        return
    
    is_exists = resume_repository.is_exist(message.from_user.id)    
    if is_exists:
        await bot.send_message(message.chat.id, text=BotMessages['file_upload_existed'])
    else:
        resume_w_data = create_resume_from_message(message, file_name)
        file: BytesIO = BytesIO()
        await message.document.download(destination=file)
        
        resume_w_data.file_data = file.read()
        
        resume_repository.create(resume_w_data)
        file.close()

        await notifier.send_registration_notification(bot, message.from_user.id)

        await bot.send_message(message.chat.id, text=BotMessages['file_upload_success'])


@dp.message_handler(commands=['question'])
async def change_state_for_question(message: types.Message):
    state = userstate_repository.get_or_create(message.from_user.id)
    if state.is_questioning:
        await bot.send_message(chat_id=message.chat.id, text=BotMessages['question_already_set'])
    else:
        userstate_repository.change_state(message.from_user.id, True)
        await bot.send_message(chat_id=message.chat.id, text=BotMessages['question_can_asked'])


@dp.message_handler(commands=['help'])
async def help_info(message: types.Message):
    is_resume_exist = resume_repository.is_exist(message.from_user.id)
    if is_resume_exist:
        status = BotMessages['help_header_existed']
    else:
        status = BotMessages['help_header_new']

    change_resume = BotMessages['help_body']
    status_msg = status + change_resume
    
    await bot.send_message(message.chat.id, text=status_msg)
    

@dp.message_handler(commands=['delete_resume'])
async def delete_resume(message: types.Message):
    resume = resume_repository.get_by_user_id(message.from_user.id)
    if resume is None:
        await bot.send_message(chat_id=message.chat.id, text=BotMessages['delete_resume_empty'])
    else:
        resume_repository.delete(resume.id)
        await bot.send_message(chat_id=message.chat.id, text=BotMessages['delete_resume_success'])


@dp.message_handler()
async def user_messages_handler(message: types.Message):
    user_state = userstate_repository.get(message.from_user.id)
    if user_state is None:
        await bot.send_message(chat_id=message.chat.id, text=BotMessages['message_error'])
    elif user_state.is_questioning:
        await handle_question(message)
    else:
        await bot.send_message(chat_id=message.chat.id, text=BotMessages['message_error'])



def is_resume_extension_valid(ext: str) -> bool:
    valid_exts = ['.pdf', '.rtf', '.docx', '.doc', '.pages']
    if ext in valid_exts:
        return True
    else:
        return False


def set_user_from_message(message: types.Message) -> User:
    user = User(
        id = message.from_user.id,
        first_name = message.from_user.first_name,
        last_name = message.from_user.last_name,
        username = message.from_user.username,
        created_at = datetime.now(tz=timezone.utc),
    )

    return user


def create_resume_from_message(message: types.Message, file_name: Path) -> Resume:    
    return Resume(
        user_id = message.from_user.id,
        filename = file_name.name,
        extension = file_name.suffix,
        file_data = "",
        created_at = datetime.now(tz=timezone.utc),
    )

async def handle_question(message: types.Message):
    await notifier.send_question_from_user(bot, message.message_id, message.chat.id)
    userstate_repository.change_state(message.from_user.id, False)
    await bot.send_message(chat_id=message.chat.id, text=BotMessages['question_will_answered'])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
