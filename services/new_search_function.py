import aiohttp
import asyncio
from bs4 import BeautifulSoup
from services.search_function import bot
from database.database import users_requests_db
from config_data.config import admin_id


async def new_search(session: aiohttp.ClientSession, sem, user_id, request):
    async with sem:
        url = request['request']
        if not request['request'].startswith('https:'):
            url = f"https://www.kufar.by/l{request['region']}?cmp=0&ot=1&query={request['request']}&sort=lst.d"
        async with session.get(url) as response:
            resp = await response.text()
            soup = BeautifulSoup(resp, 'html.parser')
            items = soup.find_all('section')[:4]
            for item in items:
                price = item.find('p').text
                if '$' in price:
                    price = price.split('р.')[1]
                try:
                    name = item.find('h3').text
                except Exception:
                    await bot.send_message(admin_id, url)
                city = item.find_all('p')[1].text
                link = item.find('a')['href'].split('?')[0]
                message = f'{price}\n{name}\n{city}\n{link}'
                if "<" in message or ">" in message:
                    message = message.replace(">", "&gt;").replace("<", "&lt;")
                if message not in request['user_items']:
                    request['user_items'].append(message)
                    try:
                        img = item.find('img')['data-src']
                        await bot.send_photo(chat_id=user_id, photo=img, caption=message)
                    except Exception as err:
                        print(err)
                        try:
                            await bot.send_message(chat_id=user_id, text=message)
                        except Exception as e:
                            print(e)


async def new_search_monitor(num_sem):
    sem = asyncio.Semaphore(num_sem)
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(new_search(session, sem, user_id, request))
                 for user_id, request in users_requests_db.copy().items()]
        await asyncio.gather(*tasks)
