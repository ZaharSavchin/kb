from aiogram import Router, F
from aiogram.types import Message

from config_data.config import admin_id

from database.database import users_db

from handlers.admin_handlers import bot
from config_data.logging_utils import logger

router = Router()


@router.message(F.text == 'bot send ads to users')
@logger.catch
async def send_ads(message: Message):
    counter = 0
    for user_id, name in users_db.copy().items():
        if "<" in name or ">" in name:
            name = name.replace(">", "&gt;").replace("<", "&lt;")
        try:
            await bot.send_photo(chat_id=user_id, photo='https://img.freepik.com/premium-vector/cute-raccoon-driving-a-racing-car_471222-1363.jpg',
                                 caption=f'Здравствуйте <b>{name}</b>👋\n\n'
                                         f'Переходите в новый чат-бот и отслеживайте объявления на сайте av.by!\n\n'
                                         f'@EnotAvBot',
                                 parse_mode='HTML')
            counter += 1
        except Exception:
            await bot.send_message(chat_id=admin_id, text=f'{user_id}, {name} недоступен')

    await bot.send_message(chat_id=admin_id, text=f'{counter} сообщений доставлено')



