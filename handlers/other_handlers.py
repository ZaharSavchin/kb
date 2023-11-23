from aiogram import Router
from aiogram.filters import Text
from aiogram.types import Message, CallbackQuery
from lexicon.lexicon import LEXICON
from config_data.logging_utils import logger
from config_data.config import admin_id
from handlers.admin_handlers import bot
from database.database import users_db, usernames_db

router = Router()


@router.callback_query(Text(text='slots'))
@logger.catch
async def by_slots(callback: CallbackQuery):
    user_id = callback.from_user.id
    await callback.message.answer(text=f' - Количество запросов = количество слотов (ячеек для отслеживания)\n'
                                       f' - <b>Один</b> слот бесплатный с частотой отслеживания около <b>30 минут</b>\n'
                                       f' - <b>Второй</b> слот стоит 5 BYN в месяц\n'
                                       f' - <b>Каждый</b> последующий 2.5 BYN в месяц\n'
                                       f' - При добавлении любого количества слотов частота отслеживания всех запросов и ссылок (включая первый бесплатный) около <b>1 минуты</b>\n\n'
                                       f' - Для получения реквизитов для оплаты напишите сюда @help_enot нужное Вам количество слотов')
    mes_too_admin = f'{users_db[user_id]}, @{usernames_db[user_id]}, {user_id}'.replace(">", "&gt;").replace("<", "&lt;")
    await bot.send_message(chat_id=admin_id, text=mes_too_admin)
    await callback.answer()


@router.message()
@logger.catch
async def unknown_message(message: Message):
    await message.answer(LEXICON["/help"])
