import logging
from aiogram import Router, F
from aiogram.types import Message
from database.database import users_requests_db, users_db
from services.search_function import get_items
from config_data.logging_utils import setup_logger

setup_logger('app.log')


router = Router()


@router.message(F.text.startswith('bot stat'))
async def stat_message(message: Message):
    try:
        if message.text.endswith('start'):
            await get_items()
        elif message.text.endswith('all'):
            message_dict = {}

            for k, v in users_db.copy().items():
                message_dict[v] = ""

            for key, value in users_requests_db.copy().items():
                message_dict[value['name']] = value['request']

            answer = [f"{k}: {v}\n" for k, v in message_dict.items()]

            stat = ''.join(answer)
            await message.answer(f"{stat}users: {len(users_db)}\nactive users: {len(users_requests_db)}")
            print(users_requests_db)
        else:
            await message.answer(f"users: {len(users_db)}\nactive users: {len(users_requests_db)}")
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")