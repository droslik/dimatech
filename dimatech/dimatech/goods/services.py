from sanic import response
from sanic.exceptions import SanicException
from goods.crud import get_goods_item_by_title, create_new_goods_item, get_goods_item_by_id
from users.crud import get_user_accounts_from_db, update_account_balance
from users.services import get_user_id_by_token


async def create_goods_service(request):
    goods_item = {
        'title': request.form['title'][0] if 'title' in request.form else request.json['title'],
        'description': request.form['description'][0] if 'description' in request.form else request.json['description'],
        'price': request.form['price'][0] if 'price' in request.form else request.json['price']
    }
    title = goods_item['title']
    db_goods_item = await get_goods_item_by_title(request, title)
    if db_goods_item:
        raise SanicException(
            status_code=400,
            message=f"item with name:{title} already exists"
        )
    return await create_new_goods_item(request, goods_item)


async def buy_goods_item(request, id: int):
    goods_item_db = await get_goods_item_by_id(request, id)
    user_id = await get_user_id_by_token(request)
    if not isinstance(user_id, int):
        return response.json({'message': user_id})
    if goods_item_db:
        price = goods_item_db.price
        accounts = await get_user_accounts_from_db(request, user_id)
        if not accounts:
            return response.json({'message': 'you do not have any account'})
        for account in accounts:
            bill_id = account.bill_id
            balance = account.balance
            if balance >= price:
                new_balance = balance - price
                message = await update_account_balance(request, bill_id, new_balance)
                return response.json({'message': message})
        return response.json({'message': 'you do not have enough money on your accounts'})

