from users.auth import login
from users.handlers import (
    create_user,
    hello,
    get_all_users,
    get_user,
    activate_user,
    get_accounts,
    get_own_page,
    my_accounts,
    change_state
)


users_urls = [
    {'uri': '/users/create_user/', 'handler': create_user, 'methods': ['POST']},
    {'uri': '/', 'handler': hello, 'methods': ['GET']},
    {'uri': '/users/all/', 'handler': get_all_users, 'methods': ['GET']},
    {'uri': '/users/<id>/', 'handler': get_user, 'methods': ['GET']},
    {'uri': '/users/<id>/change_user_state/', 'handler': change_state, 'methods': ['PATCH']},
    {'uri': '/users/own_page/', 'handler': get_own_page, 'methods': ['GET']},
    {'uri': '/users/own_page/accounts/', 'handler': my_accounts, 'methods': ['GET', 'POST']},
    {'uri': '/users/<id>/accounts/', 'handler': get_accounts, 'methods': ['GET']},
    {'uri': 'users/activate/<username>/<id>/<secret>', 'handler': activate_user, 'methods': ['GET']},
    {'uri': '/auth/login/', 'handler': login, 'methods': ['POST']},
]
