from goods.handlers import (
    create_goods,
    view_goods,
    get_goods_item,
    update_goods_item,
    delete_goods_item,
    buy_goods
)

goods_urls = [
    {'uri': '/goods/', 'handler': view_goods, 'methods': ['GET']},
    {'uri': '/goods/create/', 'handler': create_goods, 'methods': ['POST']},
    {'uri': '/goods/<id>/', 'handler': get_goods_item, 'methods': ['GET']},
    {'uri': '/goods/<id>/delete/', 'handler': delete_goods_item, 'methods': ['DELETE']},
    {'uri': '/goods/<id>/update/', 'handler': update_goods_item, 'methods': ['PATCH']},
    {'uri': '/goods/<id>/buy/', 'handler': buy_goods, 'methods': ['PATCH']},
]
