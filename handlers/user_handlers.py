from aiogram import Router

from aiogram import F
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command, CommandStart

from handlers.admin_handlers import bot
from lexicon.lexicon import LEXICON, LEXICON_REGIONS
from database.database import users_requests_db, users_db, save_users_db, save_users_requests_db, \
    usernames_db, save_usernames_db, users_max_items, save_users_max_items
from keyboards.regions_kb import create_regions_keyboard
from config_data.config import admin_id
from config_data.logging_utils import logger


router = Router()

button = InlineKeyboardButton(text='Добавить слоты и ускорить отслеживание', callback_data='slots')
slots_button = InlineKeyboardMarkup(inline_keyboard=[[button]])


@logger.catch
async def start_notification(user_id, name, username):
    if user_id not in users_db:
        try:
            await bot.send_message(chat_id=admin_id, text=f'{name}, @{username} присоединился')
        except Exception as err:
            print(err)


@logger.catch
async def extract_unique_code(text):
    # Extracts the unique_code from the sent /start command.
    return text.split()[1] if len(text.split()) > 1 else None


@router.message(CommandStart())
@logger.catch
async def process_start_command(message: Message):
    if message.from_user.id not in users_max_items:
        users_max_items[message.from_user.id] = 1
        await save_users_max_items()
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
@logger.catch
async def process_help_command(message: Message):
    usernames_db[message.from_user.id] = message.from_user.username
    await save_usernames_db()
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = message.from_user.full_name
    await message.answer(LEXICON["/help"], reply_markup=slots_button)


@router.message(Command(commands='slots'))
@logger.catch
async def buy_button(message: Message):
    user_id = message.from_user.id
    await message.answer(text=f' - Количество запросов (ссылок) = количество слотов (ячеек для отслеживания)\n'
                              f' - <b>Один</b> слот у Вас есть сразу с частотой отслеживания около <b>30 минут</b>\n'
                              f' - При добавлении любого количества слотов частота отслеживания всех слотов (включая первый) около <b>1 минуты</b>\n\n'
                              f' - Для добавления напишите сюда @help_enot нужное Вам количество слотов')
    mes_too_admin = f'{users_db[user_id]}, @{usernames_db[user_id]}, {user_id}'.replace(">", "&gt;").replace("<", "&lt;")
    await bot.send_message(chat_id=admin_id, text=mes_too_admin)


@router.message(Command(commands='donat'))
@logger.catch
async def process_donat_command(message: Message):
    usernames_db[message.from_user.id] = message.from_user.username
    await save_usernames_db()
    users_db[message.from_user.id] = message.from_user.full_name
    await message.answer(LEXICON["/donat"])


@router.message(Command(commands='stop'))
@logger.catch
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


class DeleteCallbackFactory(CallbackData, prefix='itm'):
    item: str
    reg: str


@router.message(Command(commands='list'))
@logger.catch
async def get_list_of_items(message: Message):
    user_id = message.from_user.id

    if user_id not in users_requests_db:
        await message.answer('У Вас ничего не отслеживается\n'
                             'отправьте боту запрос или ссылку для отслеживания')
        await message.answer(f'всего слотов для отслеживания: {users_max_items[user_id]}\n',
                             reply_markup=slots_button)
    else:
        for req, reg in zip(users_requests_db[user_id]['request'], users_requests_db[user_id]['region']):
            request_ = req
            reg_ = reg
            if reg_ != '':
                reg_ = reg_[5]+reg_[-1]
            if len(request_) > 30:
                request_ = request_[-30:]
            if ':' in request_:
                request_ = request_.replace(':', '≝')
                print(len(request_))
            try:
                button = InlineKeyboardButton(text=f"Удалить",
                                              callback_data=DeleteCallbackFactory(item=request_,
                                                                                  reg=reg_).pack())
            except ValueError as err:
                print(f'{DeleteCallbackFactory} = {err}')
                request_ = request_[-5:]
                button = InlineKeyboardButton(text=f"Удалить",
                                              callback_data=DeleteCallbackFactory(item=request_,
                                                                                  reg=reg_).pack())
            markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
            if "<" in req or ">" in req:
                req = req.replace(">", "&gt;").replace("<", "&lt;")
            if req.startswith('https:') and 'kufar' in req:
                await message.answer(f'{req} (прямая ссылка)', reply_markup=markup)
            else:
                await message.answer(f'{req} ({LEXICON_REGIONS[reg]})', reply_markup=markup)
        await message.answer(f'всего слотов для отслеживания: {users_max_items[user_id]}\n'
                             f'свободных слотов: {users_max_items[user_id] - len(users_requests_db[user_id]["request"])}',
                             reply_markup=slots_button)


@router.message(F.text == 'my id')
@logger.catch
async def get_my_id(message: Message):
    await message.answer(f'{message.from_user.id}')


@router.message(F.text)
@logger.catch
async def add_request_process(message: Message):
    user_id = message.from_user.id

    full_name = message.from_user.full_name
    if "<" in full_name or ">" in full_name:
        full_name = full_name.replace(">", "&gt;").replace("<", "&lt;")
    users_db[user_id] = full_name
    await save_users_db()

    username = message.from_user.username
    if username:
        if "<" in username or ">" in username:
            username = username.replace(">", "&gt;").replace("<", "&lt;")
    usernames_db[user_id] = username

    logger.info(f'@{username}, {full_name}, {user_id} = {message.text}')

    await save_usernames_db()

    if user_id not in users_requests_db:
        full_name = message.from_user.full_name
        if "<" in full_name or ">" in full_name:
            full_name = full_name.replace(">", "&gt;").replace("<", "&lt;")
        users_requests_db[user_id] = {'name': full_name,
                                      'request': [],
                                      'region': [],
                                      'user_items': []}
    if user_id in users_requests_db and len(users_requests_db[user_id]['request']) < users_max_items[user_id]:
        users_requests_db[user_id]['request'].append(message.text)
        users_requests_db[user_id]['region'].append('')
        if message.text.startswith("https:"):
            mess = message.text
            if "<" in mess or ">" in mess:
                mess = mess.replace(">", "&gt;").replace("<", "&lt;")
            await message.answer(text=f"Начат поиск по ссылке: {mess}\n✉️ожидайте сообщений...", reply_markup=slots_button)
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

    else:
        await message.answer('У Вас недостаточно слотов,'
                             ' удалите неактуальные запросы в /list или перезапустите бота /start', reply_markup=slots_button)
