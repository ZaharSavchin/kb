from handlers.user_handlers import DeleteCallbackFactory
from aiogram import Router
from aiogram.types import CallbackQuery
from database.database import users_requests_db, save_users_requests_db


router = Router()


@router.callback_query(DeleteCallbackFactory.filter())
async def delete_press(callback: CallbackQuery,
                       callback_data: DeleteCallbackFactory):
    user_id = callback.from_user.id
    item = callback_data.item
    if '≝' in item:
        item = item.replace('≝', ':')
    region = callback_data.reg
    if user_id in users_requests_db:
        index = 0
        for request, region_ in zip(users_requests_db[user_id]['request'], users_requests_db[user_id]['region']):
            if region_ != '':
                region_ = region_[5]+region_[-1]
            if len(request) > len(item):
                request = request[-len(item):]
            print(f'{item} == {request}, {region} == {region_}')
            if item == request and region == region_:
                del users_requests_db[user_id]['request'][index]
                del users_requests_db[user_id]['region'][index]
                if len(users_requests_db[user_id]['request']) == 0:
                    del users_requests_db[user_id]
                break
            index += 1
    await callback.message.delete()
    await save_users_requests_db()
