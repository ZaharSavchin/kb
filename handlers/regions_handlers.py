from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import CallbackQuery, Message
from database.database import users_requests_db


router = Router()


@router.callback_query(Text(text='all'))
async def process_forward_press(callback: CallbackQuery):
    users_requests_db[callback.from_user.id]['region'] = ''
    await callback.answer(f"Начат поиск по запросу {users_requests_db[callback.from_user.id]['request']}")



@router.callback_query(Text(text='/r~minsk'))
async def minsk(callback: CallbackQuery):
    users_requests_db[callback.from_user.id]['region'] = '/r~minsk'
    await callback.answer(f"Начат поиск по запросу {users_requests_db[callback.from_user.id]['request']}")


@router.callback_query(Text(text='/r~minskaya-obl'))
async def minsk_obl(callback: CallbackQuery):
    users_requests_db[callback.from_user.id]['region'] = '/r~minskaya-obl'
    await callback.answer(f"Начат поиск по запросу {users_requests_db[callback.from_user.id]['request']}")



@router.callback_query(Text(text='/r~brestskaya-obl'))
async def brest(callback: CallbackQuery):
    users_requests_db[callback.from_user.id]['region'] = '/r~brestskaya-obl'
    await callback.answer(f"Начат поиск по запросу {users_requests_db[callback.from_user.id]['request']}")


@router.callback_query(Text(text='/r~grodnenskaya-obl'))
async def grodno(callback: CallbackQuery):
    users_requests_db[callback.from_user.id]['region'] = '/r~grodnenskaya-obl'
    await callback.answer(f"Начат поиск по запросу {users_requests_db[callback.from_user.id]['request']}")


@router.callback_query(Text(text='/r~mogilevskaya-obl'))
async def mogilev(callback: CallbackQuery):
    users_requests_db[callback.from_user.id]['region'] = '/r~mogilevskaya-obl'
    await callback.answer(f"Начат поиск по запросу {users_requests_db[callback.from_user.id]['request']}")


@router.callback_query(Text(text='/r~vitebskaya-obl'))
async def vitebsk(callback: CallbackQuery):
    users_requests_db[callback.from_user.id]['region'] = '/r~vitebskaya-obl'
    await callback.answer(f"Начат поиск по запросу {users_requests_db[callback.from_user.id]['request']}")


@router.callback_query(Text(text='/r~gomelskaya-obl'))
async def gomel(callback: CallbackQuery):
    users_requests_db[callback.from_user.id]['region'] = '/r~gomelskaya-obl'
    await callback.answer(f"Начат поиск по запросу {users_requests_db[callback.from_user.id]['request']}")
