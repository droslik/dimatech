import jwt
from functools import wraps
from sanic import json
from settings import Settings
from users.crud import get_user_by_id


def admin_permission(wrapped):
    def decorator(f):
        @wraps(f)
        async def decorated_func(request, *args, **kwargs):
            is_admin = await check_admin(request)
            if is_admin:
                response = await f(request, *args, **kwargs)
                return response
            else:
                return json(
                    {'message': 'you do not have permission for such action'}
                )
        return decorated_func
    return decorator(wrapped)


async def check_admin(request):
    token = request.headers['token'] if 'token' in request.headers else request.token
    try:
        encoded = jwt.decode(
            token, Settings.JWT_SECRET_KEY, algorithms=Settings.ALGORITHM
        )
        user_id = encoded['sub']
        user_from_db = await get_user_by_id(request, user_id)
        if user_from_db['is_admin'] is True:
            return True
    except jwt.exceptions.InvalidTokenError:
        return False


def owner_or_admin_permission(wrapped):
    def decorator(f):
        @wraps(f)
        async def decorated_func(request, *args, **kwargs):
            is_admin_or_owner = await check_owner_or_admin(
                request, *args, **kwargs
            )
            if is_admin_or_owner:
                response = await f(request, *args, **kwargs)
                return response
            else:
                return json(
                    {'message': 'You do not have permission for suc action'}
                )

        return decorated_func

    return decorator(wrapped)


async def check_owner_or_admin(request, *args, **kwargs):
    token = request.headers['token'] if 'token' in request.headers else request.token
    owner_id = kwargs['id']
    try:
        encoded = jwt.decode(
            token, Settings.JWT_SECRET_KEY, algorithms=Settings.ALGORITHM
        )
        user_id = encoded['sub']
        user_from_db = await get_user_by_id(request, user_id)
        if user_from_db['is_admin'] == True or owner_id == user_id:
            return True
    except jwt.exceptions.InvalidTokenError:
        return False
