from sanic import response
from sanic_ext import openapi
from users.crud import (
    get_user_by_id,
    get_all_users_from_db,
    get_user_accounts_from_db,
    create_user_account,
    update_user
)
from users.services import (
    user_activation,
    create_user_service,
    get_user_id_by_token
)
from permissions import admin_permission
from users.schema import UserSchema


# url /
async def hello(request):
    return response.json({'message': 'Welcome to page'})


# url /users/create_user/
@openapi.body(UserSchema)
async def create_user(request):
    return await create_user_service(request)


# url users/activate/<username>/<id>/<secret>
async def activate_user(request, username, id: int, secret):
    return await user_activation(request, username, id, secret)


# url /users/all/
@openapi.parameter('token', str, 'header', required=True)
@admin_permission
async def get_all_users(request):
    users_db = await get_all_users_from_db(request)
    return response.json(
        {'users': [
            {'id': user_db['id'],
             'username': user_db['username'],
             'is_active': user_db['is_active']
             } for user_db in users_db]})


# url /users/<id>/
@openapi.parameter('token', str, 'header', required=True)
@admin_permission
async def get_user(request, id: int):
    user = await get_user_by_id(request, id)
    return response.json(
        {'user': {
            'id': user['id'],
            'username': user['username'],
            'is_active': user['is_active']
        }}
    )


# url /users/own_page/
@openapi.parameter('token', str, 'header', required=True)
async def get_own_page(request):
    user_id = await get_user_id_by_token(request)
    if isinstance(user_id, int):
        user = await get_user_by_id(request, user_id)
        return response.json({'user': {**user}})
    return response.json({'message': user_id})


# url /users/own_page/accounts/
@openapi.parameter('token', str, 'header', required=True)
async def my_accounts(request):
    user_id = await get_user_id_by_token(request)
    if isinstance(user_id, int):
        if request.method == 'POST':
            created_accounts = await create_user_account(request, user_id)
            return response.json({'account_created': {**created_accounts}})
        if request.method == 'GET':
            accounts_db = await get_user_accounts_from_db(request, user_id)
            if accounts_db:
                return response.json({'accounts': [{**account_db} for account_db in accounts_db]})
            return response.json({'message': 'You have no any account',
                                  'status_code': 404})
    return response.json({'message': user_id})


# url /users/<id>/accounts/
@openapi.parameter('token', str, 'header', required=True)
@admin_permission
async def get_accounts(request, id: int):
    user_id = id
    accounts_db = await get_user_accounts_from_db(request, user_id)
    if accounts_db:
        return response.json({'accounts': [{**account_db} for account_db in accounts_db]})
    return response.json({'message': 'You have no any account',
                          'status_code': 404})


# url /users/<id>/change_user_state/
@openapi.parameter('token', str, 'header', required=True)
@admin_permission
async def change_state(request, id: int):
    update_message = await update_user(request, id)
    return response.json({'message': update_message})
