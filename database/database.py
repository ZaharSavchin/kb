from typing import Dict, List, Union

import redis
import json
import logging

users_db: Dict[int, str] = {}
# users_db: Dict[int: str] = {id: full_name, ....}

users_requests_db: Dict[int, Dict[str, Union[str, List[str]]]] = {}
# users_requests_db: Dict[int, Dict[str, Union[str, List[str]]]] = {
#     686811658: {
#         'full_name': 'Nikolay Sirosh',
#         'request': 'iphone',
#         'user_items': ['itm1', 'itm2', 'itm3']
#     },
#     965855365: {
#         'full_name': 'MaxKurnickiy',
#         'request': 'лодка',
#         'region': ''
#         'user_items': ['itm1', 'itm2', 'itm3']

try:
    # Подключение к Redis
    # r = redis.Redis(host='localhost', port=6379, db=1)
    r = redis.Redis(host='94.26.236.11', port=6379, db=0)

    # Получение словаря из Redis
    user_dict_json = r.get('user_dict')
    if user_dict_json is not None:
        users_db = json.loads(user_dict_json)
        users_db = {int(k): v for k, v in users_db.items()}
    else:
        users_db = {}

    user_requests_json = r.get('users_requests')
    if user_requests_json is not None:
        users_requests_db = json.loads(user_requests_json)
        users_requests_db = {int(k): v for k, v in users_requests_db.items()}
    else:
        users_requests_db = {}
except Exception as e:
    logging.error(f"Произошла ошибка: {e}")


# Функция для сохранения словаря в Redis
async def save_users_db():
    r.set('user_dict', json.dumps(users_db))


async def save_users_requests_db():
    r.set('users_requests', json.dumps(users_requests_db))





