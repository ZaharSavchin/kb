import asyncio

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config, admin_id
from keyboards.main_menu import set_main_menu
from handlers import other_handlers, user_handlers, admin_handlers, regions_handlers, ads_handler


async def main():
    config: Config = load_config()

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

    try:
        await bot.send_message(chat_id=admin_id, text='бот перезапущен')
    except Exception as err:
        print(err)

    dp = Dispatcher()

    await set_main_menu(bot)

    dp.include_router(ads_handler.router)
    dp.include_router(admin_handlers.router)
    dp.include_router(user_handlers.router)
    dp.include_router(regions_handlers.router)
    dp.include_router(other_handlers.router)

    await dp.start_polling(bot, polling_timeout=30)


if __name__ == '__main__':
    asyncio.run(main())
