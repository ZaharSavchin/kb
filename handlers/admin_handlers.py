import asyncio

from aiogram.filters import Text

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from database.database import users_requests_db, users_db, save_users_db, save_users_requests_db, usernames_db
from services.search_function import get_items, test_time
from keyboards.delete_kb import create_delete_users_keyboard

from config_data.config import Config, load_config
from aiogram import Bot


API_URL: str = 'https://api.telegram.org/bot'
config: Config = load_config()
BOT_TOKEN = config.tg_bot.token
bot = Bot(token=BOT_TOKEN, parse_mode='HTML')


router = Router()


users_to_delete = {}


@router.message(F.text.startswith('bot stat'))
async def stat_message(message: Message):
    if message.text.endswith('start'):
        await get_items()
    elif message.text.endswith('all'):
        answer = []
        counter = 1
        for i in users_db.copy():
            if i in users_requests_db:
                if i in usernames_db:
                    name = users_db[i]
                    if "<" in name or ">" in name:
                        name = name.replace(">", "&gt;").replace("<", "&lt;")
                    answer.append(
                        f"{counter}){name}(@{usernames_db[i]}): {users_requests_db[i]['request']}✅\n")
                else:
                    name = users_db[i]
                    if "<" in name or ">" in name:
                        name = name.replace(">", "&gt;").replace("<", "&lt;")  # Замените "<*>" на "&lt;*&gt;" для правильной обработки
                    answer.append(f"{counter}){name}: {users_requests_db[i]['request']}✅\n")
                counter += 1
            else:
                if i in usernames_db:
                    name = users_db[i]
                    if "<" in name or ">" in name:
                        name = name.replace(">", "&gt;").replace("<", "&lt;")
                    answer.append(f"{counter}){name}(@{usernames_db[i]}): 🤷\n")
                else:
                    name = users_db[i]
                    if "<" in name or ">" in name:
                        name = name.replace(">", "&gt;").replace("<", "&lt;")  # Замените "<*>" на "&lt;*&gt;" для правильной обработки
                    answer.append(f"{counter}){name}: 🤷\n")
                counter += 1
        message_long = 50
        if len(answer) > message_long:
            messages = len(answer) // message_long
            last_user = len(answer) % message_long
            counter = 0
            for i in range(messages + 1):
                stat = ''.join(answer[counter: counter+message_long])
                counter += message_long
                await message.answer(f"{stat}")
                await asyncio.sleep(0.01)
            stat = ''.join(answer[counter: counter + last_user])
            # await message.answer(f"{stat}")
            await message.answer(f"users: {len(users_db)}\nactive users: {len(users_requests_db)}")
        else:
            stat = ''.join(answer)
            await message.answer(f"{stat}users: {len(users_db)}\nactive users: {len(users_requests_db)}")
        # print(users_requests_db)
    else:
        await message.answer(f"users: {len(users_db)}\nactive users: {len(users_requests_db)}")


async def clear_users(user_id, name):
    if "<" in name or ">" in name:
        name = name.replace(">", "&gt;").replace("<", "&lt;")
    try:
        sent_message = await bot.send_message(chat_id=user_id, text="_", disable_notification=True)
        await bot.delete_message(chat_id=user_id, message_id=sent_message.message_id)
    except Exception as e:
        print(e)
        users_to_delete[user_id] = name
        # await asyncio.sleep(0.05)
    # print(users_to_delete)


@router.message(F.text == 'bot users clear')
async def delete(message: Message):
    tasks = [asyncio.create_task(clear_users(user_id, name)) for user_id, name in users_db.copy().items()]
    await asyncio.gather(*tasks)

    message_dict = {}

    for k, v in users_to_delete.items():
        if k in users_db:
            message_dict[v] = ""

        if k in users_requests_db:
            message_dict[v] = users_requests_db[k]['request']

    answer = [f"{k}: {v}\n" for k, v in message_dict.items()]

    stat = ''.join(answer)
    await message.answer(
        f"{stat}users to delete: {len(users_to_delete)}",
        reply_markup=create_delete_users_keyboard('delete',
                                                  'cansel'))



# @router.message(F.text == 'bot users clear')
# async def clear_users(message: Message):
#     for user_id, name in users_db.copy().items():
#         if "<" in name or ">" in name:
#             name = name.replace(">", "&gt;").replace("<", "&lt;")
#         try:
#             sent_message = await bot.send_message(chat_id=user_id, text="_", disable_notification=True)
#             await bot.delete_message(chat_id=user_id, message_id=sent_message.message_id)
#         except Exception as e:
#             print(e)
#             users_to_delete[user_id] = name
#         # await asyncio.sleep(0.05)
#     # print(users_to_delete)
#
#     message_dict = {}
#
#     for k, v in users_to_delete.items():
#         if k in users_db:
#             message_dict[v] = ""
#
#         if k in users_requests_db:
#             message_dict[v] = users_requests_db[k]['request']
#
#     answer = [f"{k}: {v}\n" for k, v in message_dict.items()]
#
#     stat = ''.join(answer)
#     await message.answer(
#         f"{stat}users to delete: {len(users_to_delete)}",
#         reply_markup=create_delete_users_keyboard('delete',
#                                                   'cansel'))


@router.callback_query(Text(text='delete'))
async def delete(callback: CallbackQuery):
    id_to_delete = set(users_db.keys()) & set(users_to_delete.keys())

    for key in id_to_delete:
        users_db.pop(key, None)
        users_requests_db.pop(key, None)

    users_to_delete.clear()
    await callback.answer("Недоступные пользователи удалены")
    await save_users_requests_db()
    await save_users_db()


@router.callback_query(Text(text='cansel'))
async def cansel(callback: CallbackQuery):
    users_to_delete.clear()
    await callback.answer("удаление отменено")


@router.message(F.text == 'bot test time')
async def test_time_users(message: Message):
    await test_time()
