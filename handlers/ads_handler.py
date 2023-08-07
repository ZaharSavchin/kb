from aiogram import Router, F
from aiogram.types import Message

from database.database import users_db

from handlers.admin_handlers import bot

router = Router()


@router.message(F.text == 'bot send ads to users')
async def send_ads(message: Message):
    for user_id, name in users_db.copy().items():
        if "<" in name or ">" in name:
            name = name.replace(">", "&gt;").replace("<", "&lt;")
        try:
            await bot.send_photo(chat_id=user_id,
                                 photo='https://raw.githubusercontent.com/ZaharSavchin/images-/main/IMG_20230807_094759.jpg',
                                 caption=f'Здравствуйте <b>{name}</b>👋\n\n'
                                         f'    Если бот оказался Вам полезен, Вы можете оказать поддержку любой удобной для Вас суммой.\n'
                                         f'    Любая Ваша поддержка помогает боту оставаться бесплатным и без рекламы.\n'
                                         f'🙏Заранее Огромная Благодарность!🙏\n\n'
                                         f'<b>на номер телефона</b> (MTC): +375(29)833-49-64\n\n'
                                         f'<b>на карту:</b> (БелКарт, МИР):\n'
                                         f'номер карты: 9112 3930 4117 4546\n'
                                         f'срок действия: 06/28\n'
                                         f'имя держателя карты: VIRTUAL CARD\n\n'
                                         f'<b>через ЕРИП:</b> Банковские, финансовые услуги -> Банки, НКФО -> Белинвестбанк -> Пополнение счёта -> номер договора: 99oBYN-D85F11\n\n'
                                         f'<b>на QIWI кошелек:</b> +375 29 833 4964\n'
                                         f'http://qiwi.com/p/375298334964', parse_mode='HTML'
                                    )
        except Exception:
            await bot.send_message(chat_id=6031519620, text=f'{user_id}, {name} недоступен')



