from aiogram import Router, Bot
from aiogram.filters import Text
from aiogram.types import CallbackQuery
from database.database import users_requests_db, save_users_requests_db
from lexicon.lexicon import LEXICON_REGIONS

from config_data.config import Config, load_config
from config_data.logging_utils import logger


config: Config = load_config()

bot = Bot(token=config.tg_bot.token, parse_mode='HTML')


router = Router()


@router.callback_query(Text(text='all'))
@logger.catch
async def process_forward_press(callback: CallbackQuery):
    try:
        await callback.message.delete()
        users_requests_db[callback.from_user.id]['region'][-1] = ''
        await callback.answer()
        mess = users_requests_db[callback.from_user.id]["request"][-1]
        if "<" in mess or ">" in mess:
            mess = mess.replace(">", "&gt;").replace("<", "&lt;")
        await bot.send_message(chat_id=callback.from_user.id, text=f'🦝Енот отправился на поиски объявлений по запросу: '
                               f'"{mess}"\n'
                               f'🗺️регион: "{LEXICON_REGIONS["all"]}"\n'
                               f"✉️ожидайте сообщений...")
        await save_users_requests_db()
    except Exception as err:
        print(err)


@router.callback_query(Text(text='/r~minsk'))
@logger.catch
async def minsk(callback: CallbackQuery):
    try:
        await callback.message.delete()
        users_requests_db[callback.from_user.id]['region'][-1] = '/r~minsk'
        await callback.answer()
        mess = users_requests_db[callback.from_user.id]["request"][-1]
        if "<" in mess or ">" in mess:
            mess = mess.replace(">", "&gt;").replace("<", "&lt;")
        await bot.send_message(chat_id=callback.from_user.id, text=f'🦝Енот отправился на поиски объявлений по запросу: '
                                                                   f'"{mess}"\n'
                               f'🗺️регион: "{LEXICON_REGIONS["/r~minsk"]}"\n'
                               f"✉️ожидайте сообщений...")
        await save_users_requests_db()
    except Exception as err:
        print(err)


@router.callback_query(Text(text='/r~minskaya-obl'))
@logger.catch
async def minsk_obl(callback: CallbackQuery):
    try:
        await callback.message.delete()
        users_requests_db[callback.from_user.id]['region'][-1] = '/r~minskaya-obl'
        await callback.answer()
        mess = users_requests_db[callback.from_user.id]["request"][-1]
        if "<" in mess or ">" in mess:
            mess = mess.replace(">", "&gt;").replace("<", "&lt;")
        await bot.send_message(chat_id=callback.from_user.id, text=f'🦝Енот отправился на поиски объявлений по запросу: '
                                                                   f'"{mess}"\n'
                               f'🗺️регион: "{LEXICON_REGIONS["/r~minskaya-obl"]}"\n'
                               f"✉️ожидайте сообщений...")
        await save_users_requests_db()
    except Exception as err:
        print(err)


@router.callback_query(Text(text='/r~brestskaya-obl'))
@logger.catch
async def brest(callback: CallbackQuery):
    try:
        await callback.message.delete()
        users_requests_db[callback.from_user.id]['region'][-1] = '/r~brestskaya-obl'
        await callback.answer()
        mess = users_requests_db[callback.from_user.id]["request"][-1]
        if "<" in mess or ">" in mess:
            mess = mess.replace(">", "&gt;").replace("<", "&lt;")
        await bot.send_message(chat_id=callback.from_user.id, text=f'🦝Енот отправился на поиски объявлений по запросу: '
                                                                   f'"{mess}"\n'
                               f'🗺️регион: "{LEXICON_REGIONS["/r~brestskaya-obl"]}"\n'
                               f"✉️ожидайте сообщений...")
        await save_users_requests_db()
    except Exception as err:
        print(err)


@router.callback_query(Text(text='/r~grodnenskaya-obl'))
@logger.catch
async def grodno(callback: CallbackQuery):
    try:
        await callback.message.delete()
        users_requests_db[callback.from_user.id]['region'][-1] = '/r~grodnenskaya-obl'
        await callback.answer()
        mess = users_requests_db[callback.from_user.id]["request"][-1]
        if "<" in mess or ">" in mess:
            mess = mess.replace(">", "&gt;").replace("<", "&lt;")
        await bot.send_message(chat_id=callback.from_user.id, text=f'🦝Енот отправился на поиски объявлений по запросу: '
                                                                   f'"{mess}"\n'
                               f'🗺️регион: "{LEXICON_REGIONS["/r~grodnenskaya-obl"]}"\n'
                               f"✉️ожидайте сообщений...")
        await save_users_requests_db()
    except Exception as err:
        print(err)


@router.callback_query(Text(text='/r~mogilevskaya-obl'))
@logger.catch
async def mogilev(callback: CallbackQuery):
    try:
        await callback.message.delete()
        users_requests_db[callback.from_user.id]['region'][-1] = '/r~mogilevskaya-obl'
        await callback.answer()
        mess = users_requests_db[callback.from_user.id]["request"][-1]
        if "<" in mess or ">" in mess:
            mess = mess.replace(">", "&gt;").replace("<", "&lt;")
        await bot.send_message(chat_id=callback.from_user.id, text=f'🦝Енот отправился на поиски объявлений по запросу: '
                                                                   f'"{mess}"\n'
                               f'🗺️регион: "{LEXICON_REGIONS["/r~mogilevskaya-obl"]}"\n'
                               f"✉️ожидайте сообщений...")
        await save_users_requests_db()
    except Exception as err:
        print(err)


@router.callback_query(Text(text='/r~vitebskaya-obl'))
@logger.catch
async def vitebsk(callback: CallbackQuery):
    try:
        await callback.message.delete()
        users_requests_db[callback.from_user.id]['region'][-1] = '/r~vitebskaya-obl'
        await callback.answer()
        mess = users_requests_db[callback.from_user.id]["request"][-1]
        if "<" in mess or ">" in mess:
            mess = mess.replace(">", "&gt;").replace("<", "&lt;")
        await bot.send_message(chat_id=callback.from_user.id, text=f'🦝Енот отправился на поиски объявлений по запросу: '
                                                                   f'"{mess}"\n'
                               f'🗺️регион: "{LEXICON_REGIONS["/r~vitebskaya-obl"]}"\n'
                               f"✉️ожидайте сообщений...")
        await save_users_requests_db()
    except Exception as err:
        print(err)


@router.callback_query(Text(text='/r~gomelskaya-obl'))
@logger.catch
async def gomel(callback: CallbackQuery):
    try:
        await callback.message.delete()
        users_requests_db[callback.from_user.id]['region'][-1] = '/r~gomelskaya-obl'
        await callback.answer()
        mess = users_requests_db[callback.from_user.id]["request"][-1]
        if "<" in mess or ">" in mess:
            mess = mess.replace(">", "&gt;").replace("<", "&lt;")
        await bot.send_message(chat_id=callback.from_user.id, text=f'🦝Енот отправился на поиски объявлений по запросу: '
                                                                   f'"{mess}"\n'
                               f'🗺️регион: "{LEXICON_REGIONS["/r~gomelskaya-obl"]}"\n'
                               f"✉️ожидайте сообщений...")
        await save_users_requests_db()
    except Exception as err:
        print(err)
