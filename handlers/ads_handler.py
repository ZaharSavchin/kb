from aiogram import Router, F
from aiogram.types import Message

from database.database import users_db

from handlers.admin_handlers import bot

router = Router()


@router.message(F.text == 'bot send ads to users')
async def send_ads(message: Message):
    for user_id, name in users_db.copy().items():
        try:
            await bot.send_message(chat_id=user_id, text=f'Привет {name}👋\n\n'
                                                   f'Хочу познакомить тебя со своим братом-ботом!\n'
                                                   f'Его зовут: "Енот На Wildberries🦝"\n'
                                                   f'Его адрес: @enot_wildberries_bot\n\n'
                                                   f'Он полезен тем, что отслеживает цену на необходимый тебе товар на Wildberries.\n'
                                                   f'Ты просто отправляешь ему артикул товара и когда цена снизится он пришлет тебе уведомление👍\n\n'
                                                   f'🤓Интересный факт🤓: Иногда продавцы маркетплейсов ненадолго очень сильно снижают стоимость товара (зачастую даже ниже себестоимости) '
                                                   f'для того, что-бы повысить рейтинг карточки своего товара (увеличить количество покупок и отзывов).\n'
                                                   f'🏷️💲И что-бы не пропускать такую халяву спешит на помощь бот @enot_wildberries_bot🏷️💲')
            await bot.send_message(chat_id=user_id, text='https://t.me/enot_wildberries_bot')
        except Exception:
            await bot.send_message(chat_id=6031519620, text=f'{user_id}, {name} недоступен')



