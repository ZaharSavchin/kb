import re

import aiohttp
import asyncio
from bs4 import BeautifulSoup
from services.search_function import bot
from database.database import users_requests_db, users_max_items
from aiohttp_socks import ProxyType, ProxyConnector
from config_data.logging_utils import logger


@logger.catch
async def new_search(session: aiohttp.ClientSession, sem, user_id, request):
    async with sem:
        for reg, req in zip(request['region'], request['request']):
            try:
                url = f"https://www.kufar.by/l{reg}?cmp=0&ot=1&query={req}&sort=lst.d"
                if req.startswith('https:') and 'kufar' in req:
                    url = req
                async with session.get(url) as response:
                    resp = await response.text()
                    soup = BeautifulSoup(resp, 'html.parser')
                    sections = soup.find_all("section")[:4]
                    for section in sections:
                        section = section.find_all("a", class_=re.compile(r"styles_wrapper__[a-zA-Z0-9]+$"))
                        for element in section:
                            title = element.text
                            if len(title) > 300:
                                title = f'{title[:300]}...'
                            if "<" in title or ">" in title:
                                title = title.replace(">", "&gt;").replace("<", "&lt;")
                            link = element.get("href").split('?')[0]
                            item = f"{title}\n{link}"
                            check = item
                            if '$' in title:
                                check = link
                            if check not in request['user_items']:
                                request['user_items'].append(check)
                                if "<" in item or ">" in item:
                                    item = item.replace(">", "&gt;").replace("<", "&lt;")
                                try:

                                    image_url = re.search('data-src="(.*?)"', str(element)).group(1)
                                    await bot.send_photo(chat_id=user_id, photo=image_url, caption=item)
                                except Exception as e:
                                    print(f'e={e}')
                                    try:
                                        await bot.send_message(chat_id=user_id, text=item)
                                    except Exception as err:
                                        print(err)
            except Exception as err:
                logger.error(f'GET or SOUP err: {err}, ({url}), {user_id}')


@logger.catch
async def new_search_monitor(num_sem):
    sem = asyncio.Semaphore(num_sem)
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(new_search(session, sem, user_id, request))
                 for user_id, request in users_requests_db.copy().items()
                 if users_max_items[user_id] == 1]
        await asyncio.gather(*tasks)


@logger.catch
async def vip_new_search_monitor(num_sem):
    sem = asyncio.Semaphore(num_sem)
    connector = ProxyConnector(
        proxy_type=ProxyType.SOCKS5,  # Тип прокси (SOCKS5)
        host='185.236.20.70',  # IP-адрес прокси-сервера
        port=8000,  # Порт прокси-сервера
        username='BCYZSV',  # Имя пользователя для аутентификации
        password='UYpDQb',  # Пароль для аутентификации
        rdns=True  # Использование обратного DNS-разрешения
    )
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [asyncio.create_task(new_search(session, sem, user_id, request))
                 for user_id, request in users_requests_db.copy().items()
                 if users_max_items[user_id] > 1]
        await asyncio.gather(*tasks)
