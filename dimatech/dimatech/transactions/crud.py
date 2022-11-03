from models import transactions


async def create_transaction(request, user_id, bill_id, amount):
    data = {'user_id': user_id,
            'bill_id': bill_id,
            'amount': amount}
    query = transactions.insert().values(data)
    last_record_id = await request.app.ctx.db.execute(query)
    if last_record_id:
        transaction = await get_transaction_by_id(request, last_record_id)
        return transaction


async def get_transaction_by_id(request, id: int):
    query = transactions.select().where(transactions.c.id == id)
    transaction_db = await request.app.ctx.db.fetch_one(query=query)
    return transaction_db


async def get_transactions_by_user_id(request, user_id: int):
    query = transactions.select().where(transactions.c.user_id == user_id)
    transactions_db = await request.app.ctx.db.fetch_all(query=query)
    return transactions_db
