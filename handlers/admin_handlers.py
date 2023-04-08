from aiogram import Router, F
from aiogram.types import Message
from database.database import users_requests_db, users_db


router = Router()


@router.message(F.text.startswith('bot stat'))
async def stat_message(message: Message):

    message_dict = {}

    for k, v in users_db.items():
        message_dict[v] = ""

    for key, value in users_requests_db.items():
        message_dict[value['name']] = value['request']

    answer = [f"{k}: {v}\n" for k, v in message_dict.items()]

    stat = ''.join(answer)

    if message.text.endswith('all'):
        await message.answer(f"{stat}users: {len(users_db)}\nactive users: {len(users_requests_db)}")
    else:
        await message.answer(f"users: {len(users_db)}\nactive users: {len(users_requests_db)}")