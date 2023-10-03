import re

import aiohttp
import asyncio
from bs4 import BeautifulSoup
from services.search_function import bot
from database.database import users_requests_db
from config_data.config import admin_id


async def new_search(session: aiohttp.ClientSession, sem, user_id, request):
    async with sem:
        url = f"https://www.kufar.by/l{request['region']}?cmp=0&ot=1&query={request['request']}&sort=lst.d"
        if request['request'].startswith('https:') and 'kufar' in request['request']:
            url = request['request']
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
                        try:
                            image_url = re.search('data-src="(.*?)"', str(element)).group(1)
                            await bot.send_photo(chat_id=user_id, photo=image_url, caption=item)
                        except Exception as e:
                            print(f'e={e}')
                            try:
                                await bot.send_message(chat_id=user_id, text=item)
                            except Exception as err:
                                print(err)


async def new_search_monitor(num_sem):
    sem = asyncio.Semaphore(num_sem)
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(new_search(session, sem, user_id, request))
                 for user_id, request in users_requests_db.copy().items()]
        await asyncio.gather(*tasks)
