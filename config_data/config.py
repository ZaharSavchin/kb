from dataclasses import dataclass
from environs import Env
from config_data.logging_utils import logger

admin_id = 6031519620


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot


@logger.catch
def load_config(path: str | None = None):
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env("BOT_TOKEN")))


