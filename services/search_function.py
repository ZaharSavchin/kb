from bs4 import BeautifulSoup
import requests
import re
from database.database import users_requests_db, save_users_requests_db
import asyncio
from aiogram import Bot
from time import time
from fake_useragent import UserAgent

from config_data.config import Config, load_config, admin_id


API_URL: str = 'https://api.telegram.org/bot'
config: Config = load_config()
BOT_TOKEN = config.tg_bot.token

bot = Bot(token=config.tg_bot.token, parse_mode='HTML')


async def get_items():
    await bot.send_message(chat_id=admin_id, text='цикл запущен, start')
    while True:
        for user_id, request in users_requests_db.copy().items():
            # Запрашиваем HTML-код страницы
            if request['request'].startswith('https:'):
                result = requests.get(f"{request['request']}")
                soup = BeautifulSoup(result.text, "html.parser")
                # Получаем ссылки на последние 5 товаров
                sections = soup.find_all("section")[:2]
                for section in sections:
                    section = section.find_all("a", class_=re.compile(r"styles_wrapper__[a-zA-Z0-9]+$"))[:2]
                    for element in section:
                        title = element.text
                        if "<" in title or ">" in title:
                            title = title.replace(">", "&gt;").replace("<", "&lt;")
                        link = element.get("href")
                        item = f"{title} {link}"
                        if item[:20] not in request['user_items']:
                            request['user_items'].append(item[:20])
                            try:
                                image_url = re.search('data-src="(.*?)"', str(element)).group(1)
                                await bot.send_photo(chat_id=user_id, photo=image_url, caption=item)
                                # requests.get(
                                #     f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={user_id}&photo={image_url}&caption={item}')
                            except Exception as e:
                                print(f'e={e}')
                                try:
                                    await bot.send_message(chat_id=user_id, text=item)
                                except Exception as err:
                                    print(err)
                                # requests.get(
                                #     f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={user_id}&text={item}')
                await asyncio.sleep(0.1)
            else:
                result = requests.get(
                    f"https://www.kufar.by/l{request['region']}?cmp=0&ot=1&query={request['request']}&sort=lst.d")
                # Разбираем HTML-код с помощью BeautifulSoup
                soup = BeautifulSoup(result.text, "html.parser")
                # Получаем ссылки на последние 5 товаров
                sections = soup.find_all("section")[:4]
                for section in sections:
                    section = section.find_all("a", class_=re.compile(r"styles_wrapper__[a-zA-Z0-9]+$"))
                    for element in section:
                        title = element.text
                        if "<" in title or ">" in title:
                            title = title.replace(">", "&gt;").replace("<", "&lt;")
                        link = element.get("href")
                        item = f"{title} {link}"
                        if item[:20] not in request['user_items']:
                            request['user_items'].append(item[:20])
                            try:
                                image_url = re.search('data-src="(.*?)"', str(element)).group(1)
                                await bot.send_photo(chat_id=user_id, photo=image_url, caption=item)
                                # requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={user_id}&photo={image_url}&caption={item}')
                            except Exception as e:
                                print(f'e={e}')
                                try:
                                    await bot.send_message(chat_id=user_id, text=item)
                                except Exception as err:
                                    print(err)
                                # requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={user_id}&text={item}')
                await asyncio.sleep(0.1)
            counter += 1


async def test_time():
    counter = 1
    for user_id, request in users_requests_db.copy().items():
        start_time = time()
        # Запрашиваем HTML-код страницы
        if request['request'].startswith('https:'):
            result = requests.get(f"{request['request']}", timeout=3)
            soup = BeautifulSoup(result.text, "html.parser")
            # Получаем ссылки на последние 5 товаров
            sections = soup.find_all("section")[:2]
            for section in sections:
                section = section.find_all("a", class_=re.compile(r"styles_wrapper__[a-zA-Z0-9]+$"))[:2]
                for element in section:
                    title = element.text
                    if "<" in title or ">" in title:
                        title = title.replace(">", "&gt;").replace("<", "&lt;")
                    link = element.get("href")
                    item = f"{title} {link}"
                    if item[:20] not in request['user_items']:
                        request['user_items'].append(item[:20])
                        try:
                            image_url = re.search('data-src="(.*?)"', str(element)).group(1)
                            await bot.send_photo(chat_id=user_id, photo=image_url, caption=item)
                            # requests.get(
                            #     f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={user_id}&photo={image_url}&caption={item}')
                        except Exception as e:
                            print(f'e={e}')
                            try:
                                await bot.send_message(chat_id=user_id, text=item)
                            except Exception as err:
                                print(err)
                            # requests.get(
                            #     f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={user_id}&text={item}')
            await asyncio.sleep(0.1)
        else:
            result = requests.get(
                f"https://www.kufar.by/l{request['region']}?cmp=0&ot=1&query={request['request']}&sort=lst.d")
            # Разбираем HTML-код с помощью BeautifulSoup
            soup = BeautifulSoup(result.text, "html.parser")
            # Получаем ссылки на последние 5 товаров
            sections = soup.find_all("section")[:4]
            for section in sections:
                section = section.find_all("a", class_=re.compile(r"styles_wrapper__[a-zA-Z0-9]+$"))
                for element in section:
                    title = element.text
                    if "<" in title or ">" in title:
                        title = title.replace(">", "&gt;").replace("<", "&lt;")
                    link = element.get("href")
                    item = f"{title} {link}"
                    if item[:20] not in request['user_items']:
                        request['user_items'].append(item[:20])
                        try:
                            image_url = re.search('data-src="(.*?)"', str(element)).group(1)
                            await bot.send_photo(chat_id=user_id, photo=image_url, caption=item)
                            # requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={user_id}&photo={image_url}&caption={item}')
                        except Exception as e:
                            print(f'e={e}')
                            try:
                                await bot.send_message(chat_id=user_id, text=item)
                            except Exception as err:
                                print(err)
                            # requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={user_id}&text={item}')
            await asyncio.sleep(0.1)
        time_for_user = time() - start_time
        print(f'{counter}\n'
              f'time = {time_for_user}\n'
              f'request = {request["request"]}\n'
              f'len = {len(request["user_items"])}\n'
              f'name = {request["name"]}\n\n')
        counter += 1

