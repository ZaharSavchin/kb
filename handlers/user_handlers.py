from aiogram import Router

from aiogram import F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, Text
from lexicon.lexicon import LEXICON
from database.database import users_requests_db, users_db
# from database.database import save_users_db, save_users_requests_db
from services.search_function import get_items

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = message.from_user.full_name
        # await save_users_db()
        print(users_db)
    if message.from_user.id in users_requests_db:
        del users_requests_db[message.from_user.id]
        # await save_users_requests_db()
    await message.answer(LEXICON["/start"])


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON["/help"])


@router.message(Command(commands='stop'))
async def process_stop_command(message: Message):
    if message.from_user.id in users_requests_db:
        del users_requests_db[message.from_user.id]
        # await save_users_requests_db()
        await message.answer(LEXICON["/stop"])
    else:
        await message.answer(LEXICON["/stop"])
    print(users_requests_db)


@router.message(F.text)
async def add_request_process(message: Message):
    users_requests_db[message.from_user.id] = {'name': message.from_user.full_name,
                                               'request': message.text,
                                               'user_items': []}
    # await save_users_requests_db()
    await message.answer(f'Начат поиск по запросу "{message.text}"')
    print(users_requests_db)
    await get_items()

