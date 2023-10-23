from aiogram.exceptions import TelegramBadRequest

from handlers.admin_handlers import MaxItemsCallbackFactory
from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from database.database import (users_max_items, save_users_max_items, users_db, users_requests_db,
                               save_users_requests_db, usernames_db)
from config_data.logging_utils import logger

router = Router()


@router.callback_query(MaxItemsCallbackFactory.filter())
@logger.catch
async def plus_press(callback: CallbackQuery,
                     callback_data: MaxItemsCallbackFactory):
    user_id = callback_data.user_id
    change = callback_data.change
    if change == '+':
        users_max_items[user_id] += 1
    if change == '-':
        if users_max_items[user_id] > 1:
            users_max_items[user_id] -= 1
        if user_id in users_requests_db and len(users_requests_db[user_id]['request']) > users_max_items[user_id]:
            users_requests_db[user_id]['request'].pop(-1)
            users_requests_db[user_id]['region'].pop(-1)
        if users_max_items[user_id] == 1:
            await callback.answer()

    id_ = user_id
    name = users_db[id_]
    if "<" in name or ">" in name:
        name = name.replace(">", "&gt;").replace("<", "&lt;")
    username = f'@{usernames_db[id_]}'
    if "<" in username or ">" in username:
        username = username.replace(">", "&gt;").replace("<", "&lt;")
    slots = users_max_items[id_]
    request = 'запросов нет'
    if id_ in users_requests_db:
        request = users_requests_db[id_]['request']
    text = (f'{id_}\n'
            f'{name}, {username}\n'
            f'slots = {slots}\n'
            f'{request}')

    button_plus = InlineKeyboardButton(text='+', callback_data=MaxItemsCallbackFactory(user_id=id_, change='+').pack())
    button_minus = InlineKeyboardButton(text='-', callback_data=MaxItemsCallbackFactory(user_id=id_, change='-').pack())
    markup = InlineKeyboardMarkup(inline_keyboard=[[button_minus, button_plus]])

    try:
        await callback.message.edit_text(text=text, reply_markup=markup)
    except TelegramBadRequest as err:
        print(err)

    await callback.answer()
    await save_users_requests_db()
    await save_users_max_items()
