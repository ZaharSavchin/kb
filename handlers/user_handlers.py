from aiogram import Router

from aiogram import F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

from handlers.admin_handlers import bot
from lexicon.lexicon import LEXICON
from database.database import users_requests_db, users_db, save_users_db, save_users_requests_db, \
    usernames_db, save_usernames_db
from keyboards.regions_kb import create_regions_keyboard
from config_data.config import admin_id


router = Router()


async def start_notification(user_id, name, username):
    if user_id not in users_db:
        try:
            await bot.send_message(chat_id=admin_id, text=f'{name}, @{username} присоединился')
        except Exception as err:
            print(err)


async def extract_unique_code(text):
    # Extracts the unique_code from the sent /start command.
    return text.split()[1] if len(text.split()) > 1 else None


@router.message(CommandStart())
async def process_start_command(message: Message):
    name = message.from_user.full_name
    if "<" in name or ">" in name:
        name = name.replace(">", "&gt;").replace("<", "&lt;")
    username = message.from_user.username
    user_id = message.from_user.id
    ref_id = await extract_unique_code(message.text)
    if ref_id is None:
        await start_notification(user_id=user_id, name=name, username=username)
    if ref_id == 'wb':
        try:
            await bot.send_message(chat_id=1042048167, text=f'{name}, @{username} перешел по ссылке из @enot_wildberries_bot')
        except Exception as err:
            print(err)
    await message.answer(LEXICON["/start"])
    usernames_db[user_id] = username
    await save_usernames_db()
    if message.from_user.id not in users_db:
        users_db[user_id] = name
        await save_users_db()
    elif user_id in users_requests_db:
        del users_requests_db[user_id]
        await save_users_requests_db()


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    usernames_db[message.from_user.id] = message.from_user.username
    await save_usernames_db()
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = message.from_user.full_name
    await message.answer(LEXICON["/help"])


@router.message(Command(commands='donat'))
async def process_donat_command(message: Message):
    usernames_db[message.from_user.id] = message.from_user.username
    await save_usernames_db()
    users_db[message.from_user.id] = message.from_user.full_name
    await message.answer(LEXICON["/donat"])


@router.message(Command(commands='stop'))
async def process_stop_command(message: Message):
    usernames_db[message.from_user.id] = message.from_user.username
    await save_usernames_db()
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = message.from_user.full_name
    elif message.from_user.id in users_requests_db:
        del users_requests_db[message.from_user.id]
        await save_users_requests_db()
        await message.answer(LEXICON["/stop"])
    else:
        await message.answer(LEXICON["/stop"])


@router.message(F.text)
async def add_request_process(message: Message):
    users_db[message.from_user.id] = message.from_user.full_name
    await save_users_db()
    usernames_db[message.from_user.id] = message.from_user.username
    await save_usernames_db()
    users_requests_db[message.from_user.id] = {'name': message.from_user.full_name,
                                               'request': message.text,
                                               'region': '',
                                               'user_items': []}
    if message.text.startswith("https:"):
        await message.answer(f"Начат поиск по ссылке: {message.text}\n✉️ожидайте сообщений...")
        await save_users_requests_db()
    else:
        await message.answer(f"выберите регион поиска", reply_markup=create_regions_keyboard('all',
                                                                                             '/r~minsk',
                                                                                             '/r~minskaya-obl',
                                                                                             '/r~brestskaya-obl',
                                                                                             '/r~grodnenskaya-obl',
                                                                                             '/r~mogilevskaya-obl',
                                                                                             '/r~vitebskaya-obl',
                                                                                             '/r~gomelskaya-obl'))

        await save_users_requests_db()

