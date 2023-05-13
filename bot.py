import asyncio

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from keyboards.main_menu import set_main_menu
from handlers import other_handlers, user_handlers, admin_handlers, regions_handlers


async def main():
    config: Config = load_config()

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

    await bot.send_message(chat_id=6031519620, text='бот перезапущен')

    dp = Dispatcher()

    await set_main_menu(bot)

    dp.include_router(admin_handlers.router)
    dp.include_router(user_handlers.router)
    dp.include_router(regions_handlers.router)
    dp.include_router(other_handlers.router)

    await dp.start_polling(bot, polling_timeout=30)


if __name__ == '__main__':
    asyncio.run(main())
