from transactions.urls import transactions_urls
from goods.urls import goods_urls
from users.urls import users_urls

all_urls = [
    *users_urls,
    *goods_urls,
    *transactions_urls,
]
