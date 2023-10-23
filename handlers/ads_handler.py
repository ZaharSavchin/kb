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
            await bot.send_message(chat_id=user_id,
                                   text=f'Здравствуйте <b>{name}</b>👋\n\n'
                                        f'Теперь можно отслеживать любое количество запросов и ссылок!\n\n'
                                        f'Количество запросов = количество слотов (ячеек для отслеживания)\n'
                                        f'<b>Один</b> слот бесплатный с частотой отслеживания около <b>15 минут</b>\n'
                                        f'<b>Второй</b> слот стоит 5 бел. руб. в месяц\n'
                                        f'<b>Каждый</b> последующий 2.5 бел. руб. в месяц\n'
                                        f'При покупке любого количества слотов частота отслеживания всех запросов и ссылок (включая первый бесплатный) около <b>1 минуты</b>\n\n'
                                        f'Слоты можно оплатить через <b>ЕРИП</b>: Банковские, финансовые услуги > Банки, НКФО > Альфа-Банк > пополнение счета > +375298334964\n'
                                        f'Или просто на <b>номер телефона</b> (МТС) +375(29)833-49-64\n'
                                        f'Затем отправить <b>скриншот чека</b> и это число (<b>{user_id}</b> - это Ваш id в боте) сюда >> @help_enot\n\n'
                                        f'Слоты добавляются вручную, поэтому это происходит не мгновенно, но максимально быстро))',
                                   parse_mode='HTML'
                                   )
            counter += 1
        except Exception:
            await bot.send_message(chat_id=admin_id, text=f'{user_id}, {name} недоступен')

    await bot.send_message(chat_id=admin_id, text=f'{counter} сообщений доставлено')



