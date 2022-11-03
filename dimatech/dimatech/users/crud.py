import jwt
from passlib.context import CryptContext
from sanic import response
from models import users, accounts
from settings import Settings

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password: str) -> str:
    return password_context.hash(password)


# create user
async def create_new_user(request, user):
    username = user['username']
    hashed_password = get_password_hash(user['password'])
    data = {
        'username': username,
        'hashed_password': hashed_password,
        'is_active': False,
        'is_admin': False
    }
    query = users.insert().values(data)
    last_record_id = await request.app.ctx.db.execute(query)
    if last_record_id:
        user_db = await get_user_by_id(request, last_record_id)
        username = user_db['username']
        last_six_hash = user_db['hashed_password'][-6:]
        url = request.app.url_for(
            'activate_user',
            username=username,
            id=last_record_id,
            secret=last_six_hash
        )
        print(url)
        return response.json({'activation_link': url})


async def get_user_by_token(request):
    token = request.headers['Authorization']
    encoded = jwt.decode(
        token, Settings.JWT_SECRET_KEY, algorithms=Settings.ALGORITHM
    )
    current_user_id = encoded['sub']
    user_from_db = await get_user_by_id(request, current_user_id)
    return user_from_db


async def get_user_by_id(request, id: int):
    query = users.select().where(users.c.id == id)
    user_db = await request.app.ctx.db.fetch_one(query=query)
    return user_db


async def get_user_by_username(request, username):
    query = users.select().where(users.c.username == username)
    user_db = await request.app.ctx.db.fetch_one(query=query)
    return user_db


async def get_all_users_from_db(request):
    query = users.select()
    users_db = await request.app.ctx.db.fetch_all(query=query)
    return users_db


async def get_user_accounts_from_db(request, user_id: int):
    query = accounts.select().where(accounts.c.user_id == user_id)
    accounts_db = await request.app.ctx.db.fetch_all(query=query)
    return accounts_db


async def get_user_account_by_bill_id(request, bill_id: int):
    query = accounts.select().where(accounts.c.bill_id == bill_id)
    accounts_db = await request.app.ctx.db.fetch_one(query=query)
    return accounts_db


async def create_user_account(request, user_id):
    data = {'user_id': user_id,
            'balance': 0}
    query = accounts.insert().values(data)
    last_record_id = await request.app.ctx.db.execute(query)
    if last_record_id:
        created_accounts_db = {
            'bill_id': last_record_id,
            'balance': data['balance']
        }
        return created_accounts_db


async def update_user(request, id: int):
    user_db = await get_user_by_id(request, id)
    if not user_db:
        message = 'user does not exist'
        return message
    if user_db['is_active'] is not True:
        query = users.update().where(users.c.id == id).values(is_active=True)
        update = await request.app.ctx.db.execute(query)
        message = f'user {user_db.username} was activated'
        return message
    query = users.update().where(users.c.id == id).values(is_active=False)
    update = await request.app.ctx.db.execute(query)
    message = f'user {user_db.username} was disactivated'
    return message


async def update_account_balance(request, bill_id, new_balance):
    query = accounts.update().where(
        accounts.c.bill_id == bill_id
    ).values(balance=new_balance)
    update = await request.app.ctx.db.execute(query)
    message = f'You have successfully bought the procduct'
    return message


async def update_account_balance_transaction(request, bill_id, new_balance):
    query = accounts.update().where(
        accounts.c.bill_id == bill_id
    ).values(balance=new_balance)
    update = await request.app.ctx.db.execute(query)
