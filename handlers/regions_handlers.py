from aiogram import Router, Bot
from aiogram.filters import Text
from aiogram.types import CallbackQuery
from database.database import users_requests_db, save_users_requests_db
from lexicon.lexicon import LEXICON_REGIONS

from config_data.config import Config, load_config


config: Config = load_config()

bot = Bot(token=config.tg_bot.token, parse_mode='HTML')


router = Router()


@router.callback_query(Text(text='all'))
async def process_forward_press(callback: CallbackQuery):
    users_requests_db[callback.from_user.id]['region'] = ''
    await callback.answer()
    await bot.send_message(chat_id=callback.from_user.id, text=f'🦝Енот отправился на поиски объявлений по запросу: '
                           f'"{users_requests_db[callback.from_user.id]["request"]}"\n'
                           f'🗺️регион: "{LEXICON_REGIONS["all"]}"\n'
                           f"✉️ожидайте сообщений...")
    await save_users_requests_db()


@router.callback_query(Text(text='/r~minsk'))
async def minsk(callback: CallbackQuery):
    users_requests_db[callback.from_user.id]['region'] = '/r~minsk'
    await callback.answer()
    await bot.send_message(chat_id=callback.from_user.id, text=f'🦝Енот отправился на поиски объявлений по запросу: '
                           f'"{users_requests_db[callback.from_user.id]["request"]}"\n'
                           f'🗺️регион: "{LEXICON_REGIONS["/r~minsk"]}"\n'
                           f"✉️ожидайте сообщений...")
    await save_users_requests_db()


@router.callback_query(Text(text='/r~minskaya-obl'))
async def minsk_obl(callback: CallbackQuery):
    users_requests_db[callback.from_user.id]['region'] = '/r~minskaya-obl'
    await callback.answer()
    await bot.send_message(chat_id=callback.from_user.id, text=f'🦝Енот отправился на поиски объявлений по запросу: '
                           f'"{users_requests_db[callback.from_user.id]["request"]}"\n'
                           f'🗺️регион: "{LEXICON_REGIONS["/r~minskaya-obl"]}"\n'
                           f"✉️ожидайте сообщений...")
    await save_users_requests_db()


@router.callback_query(Text(text='/r~brestskaya-obl'))
async def brest(callback: CallbackQuery):
    users_requests_db[callback.from_user.id]['region'] = '/r~brestskaya-obl'
    await callback.answer()
    await bot.send_message(chat_id=callback.from_user.id, text=f'🦝Енот отправился на поиски объявлений по запросу: '
                           f'"{users_requests_db[callback.from_user.id]["request"]}"\n'
                           f'🗺️регион: "{LEXICON_REGIONS["/r~brestskaya-obl"]}"\n'
                           f"✉️ожидайте сообщений...")
    await save_users_requests_db()


@router.callback_query(Text(text='/r~grodnenskaya-obl'))
async def grodno(callback: CallbackQuery):
    users_requests_db[callback.from_user.id]['region'] = '/r~grodnenskaya-obl'
    await callback.answer()
    await bot.send_message(chat_id=callback.from_user.id, text=f'🦝Енот отправился на поиски объявлений по запросу: '
                           f'"{users_requests_db[callback.from_user.id]["request"]}"\n'
                           f'🗺️регион: "{LEXICON_REGIONS["/r~grodnenskaya-obl"]}"\n'
                           f"✉️ожидайте сообщений...")
    await save_users_requests_db()


@router.callback_query(Text(text='/r~mogilevskaya-obl'))
async def mogilev(callback: CallbackQuery):
    users_requests_db[callback.from_user.id]['region'] = '/r~mogilevskaya-obl'
    await callback.answer()
    await bot.send_message(chat_id=callback.from_user.id, text=f'🦝Енот отправился на поиски объявлений по запросу: '
                           f'"{users_requests_db[callback.from_user.id]["request"]}"\n'
                           f'🗺️регион: "{LEXICON_REGIONS["/r~mogilevskaya-obl"]}"\n'
                           f"✉️ожидайте сообщений...")
    await save_users_requests_db()


@router.callback_query(Text(text='/r~vitebskaya-obl'))
async def vitebsk(callback: CallbackQuery):
    users_requests_db[callback.from_user.id]['region'] = '/r~vitebskaya-obl'
    await callback.answer()
    await bot.send_message(chat_id=callback.from_user.id, text=f'🦝Енот отправился на поиски объявлений по запросу: '
                           f'"{users_requests_db[callback.from_user.id]["request"]}"\n'
                           f'🗺️регион: "{LEXICON_REGIONS["/r~vitebskaya-obl"]}"\n'
                           f"✉️ожидайте сообщений...")
    await save_users_requests_db()


@router.callback_query(Text(text='/r~gomelskaya-obl'))
async def gomel(callback: CallbackQuery):
    users_requests_db[callback.from_user.id]['region'] = '/r~gomelskaya-obl'
    await callback.answer()
    await bot.send_message(chat_id=callback.from_user.id, text=f'🦝Енот отправился на поиски объявлений по запросу: '
                           f'"{users_requests_db[callback.from_user.id]["request"]}"\n'
                           f'🗺️регион: "{LEXICON_REGIONS["/r~gomelskaya-obl"]}"\n'
                           f"✉️ожидайте сообщений...")
    await save_users_requests_db()
