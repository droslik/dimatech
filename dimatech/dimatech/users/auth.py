from datetime import timedelta, datetime
from functools import wraps
import jwt
from sanic import response, text
from sanic.exceptions import SanicException
from users.crud import get_user_by_username, password_context
from sanic_ext import openapi
from users.schema import UserSchema
from settings import Settings


def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)


@openapi.body(UserSchema)
async def login(request, *args, **kwargs):
    username = request.form['username'][0] if 'username' in request.form else request.json['username']
    password = request.form['password'][0] if 'password' in request.form else request.json['password']
    if username is None:
        raise SanicException('field username should be filled')
    user = await get_user_by_username(request, username)
    if not user:
        return response.json({'message': f'user {username} was not found'})

    if not verify_password(password, user.hashed_password):
        return response.json({'message': 'credentials provided are incorrect'})
    access_token_expires = timedelta(
        minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = await create_access_token(data={'sub': user.id}, expires_delta=access_token_expires)
    return response.json({'token': access_token, 'token_type': 'Bearer'})


async def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        Settings.JWT_SECRET_KEY,
        algorithm=Settings.ALGORITHM
    )
    return encoded_jwt


def check_token(request):
    if not request.token:
        return False
    try:
        jwt.decode(
            request.token, Settings.JWT_SECRET_KEY, algorithms=Settings.ALGORITHM
        )
    except jwt.exceptions.InvalidTokenError:
        return False
    else:
        return True


def protected(wrapped):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            is_authenticated = check_token(request)
            if is_authenticated:
                response = await f(request, *args, **kwargs)
                return response
            else:
                return text("You are unauthorized.", 401)
        return decorated_function
    return decorator(wrapped)
