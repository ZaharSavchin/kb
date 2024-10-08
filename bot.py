import asyncio

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config, admin_id
from keyboards.main_menu import set_main_menu
from handlers import (other_handlers, user_handlers, admin_handlers,
                      regions_handlers, ads_handler, change_max_items_handler,
                      delete_item_handler)
from config_data.logging_utils import logger


@logger.catch
async def main():
    config: Config = load_config()

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

    try:
        await bot.send_message(chat_id=admin_id, text='бот перезапущен')
    except Exception as err:
        logger.warning(f'admin blocked bot, {err}, bot.py line19')

    dp = Dispatcher()

    await set_main_menu(bot)

    dp.include_router(ads_handler.router)
    dp.include_router(admin_handlers.router)
    dp.include_router(user_handlers.router)
    dp.include_router(regions_handlers.router)
    dp.include_router(other_handlers.router)
    dp.include_router(change_max_items_handler.router)
    dp.include_router(delete_item_handler.router)

    await dp.start_polling(bot, polling_timeout=30)


if __name__ == '__main__':
    asyncio.run(main())
