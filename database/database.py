from typing import Dict, List, Union

import redis
import json


users_db: Dict[int, str] = {}
# users_db: Dict[int: str] = {id: full_name, ....}


usernames_db: Dict[int, str] = {}
# usernames_db: Dict[int: str] = {id: @username, ....}

users_requests_db: Dict[int, Dict[str, Union[str, List[str]]]] = {}
# users_requests_db: Dict[int, Dict[str, Union[str, List[str]]]] = {
#     686811658: {
#         'name': 'Nikolay Sirosh',
#         'request': ['iphone'],
#         'region': ['']
#         'user_items': ['itm1', 'itm2', 'itm3']
#     },
#     965855365: {
#         'full_name': 'MaxKurnickiy',
#         'request': 'лодка',
#         'region': ''
#         'user_items': ['itm1', 'itm2', 'itm3']

users_max_items: [int, int] = {}
# users_max_items: [int, int] = {5754662958: 1, 6031519620: 3}

# Подключение к Redis
# r = redis.Redis(host='localhost', port=6379, db=3)
r = redis.Redis(host='127.0.0.1', port=6379, db=1)

# Получение словаря из Redis
user_dict_json = r.get('user_dict')
if user_dict_json is not None:
    users_db = json.loads(user_dict_json)
    users_db = {int(k): v for k, v in users_db.items()}
else:
    users_db = {}


usernames_dict_json = r.get('usernames_dict')
if usernames_dict_json is not None:
    usernames_db = json.loads(usernames_dict_json)
    usernames_db = {int(k): v for k, v in usernames_db.items()}
else:
    usernames_db = {}


user_requests_json = r.get('users_requests')
if user_requests_json is not None:
    users_requests_db = json.loads(user_requests_json)
    users_requests_db = {int(k): v for k, v in users_requests_db.items()}
else:
    users_requests_db = {}

users_max_items_json = r.get('users_max_items')
if users_max_items_json is not None:
    users_max_items = json.loads(users_max_items_json)
    users_max_items = {int(k): int(v) for k, v in users_max_items.items()}
else:
    users_max_items = {}


# Функция для сохранения словаря в Redis
async def save_users_db():
    r.set('user_dict', json.dumps(users_db))


async def save_usernames_db():
    r.set('usernames_dict', json.dumps(usernames_db))


async def save_users_requests_db():
    r.set('users_requests', json.dumps(users_requests_db))


async def save_users_max_items():
    r.set('users_max_items', json.dumps(users_max_items))
