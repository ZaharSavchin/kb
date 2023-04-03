import asyncio

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from keyboards.main_menu import set_main_menu
from handlers import other_handlers, user_handlers

from aiogram.fsm.storage.redis import RedisStorage, Redis


async def main():
    config: Config = load_config()

    # redis: Redis = Redis(host='localhost')
    # storage: RedisStorage = RedisStorage(redis=redis)

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher()

    await set_main_menu(bot)

    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    # await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as err:
        print(err)

# KBjghp4q8jjm