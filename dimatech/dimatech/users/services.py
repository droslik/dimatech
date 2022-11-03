import jwt
from passlib.context import CryptContext
from sanic import response
from sanic.exceptions import SanicException
from users.crud import get_user_by_id, get_user_by_username, create_new_user
from models import users
from settings import Settings

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password):
    return password_context.hash(password)


async def create_user_service(request):
    user = {
        'username': request.form['username'][0],
        'password': request.form['password'][0],
    } if len(request.form) == 2 else {
        'username': request.json['username'],
        'password': request.json['password'],
    }
    username = user['username']
    db_user = await get_user_by_username(request, username)
    if db_user:
        raise SanicException(
            status_code=400,
            message="username is already registered"
        )
    return await create_new_user(request, user)


async def user_activation(request, username, id: int, secret):
    user_db = await get_user_by_id(request, id)
    if user_db['is_active'] is False:
        query = users.update().where(users.c.id == id).values(is_active=True)
        update = await request.app.ctx.db.execute(query)
        return response.json({'message': 'You have been activated successfully'})
    return response.json({'message': 'you have already been activated'})


async def get_user_id_by_token(request):
    token = request.headers['token'] if 'token' in request.headers else request.token
    try:
        encoded = jwt.decode(
            token, Settings.JWT_SECRET_KEY, algorithms=Settings.ALGORITHM
        )
        user_id = encoded['sub']
        user = await get_user_by_id(request, user_id)
        if user['is_active'] is not True:
            message = 'you are not activated user'
            return message
        return user_id
    except jwt.exceptions.InvalidTokenError:
        message = 'could not validate token'
        return message

