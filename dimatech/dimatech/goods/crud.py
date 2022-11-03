from sanic import response
from models import goods


async def create_new_goods_item(request, goods_item):
    query = goods.insert().values(goods_item)
    last_record_id = await request.app.ctx.db.execute(query)
    if last_record_id:
        goods_item_db = await get_goods_item_by_id(request, last_record_id)
        return response.json({'goods_item': {**goods_item_db}})


async def get_goods_item_by_id(request, id: int):
    query = goods.select().where(goods.c.id == id)
    goods_item_db = await request.app.ctx.db.fetch_one(query=query)
    return goods_item_db


async def get_goods_item_by_title(request, title: str):
    query = goods.select().where(goods.c.title == title)
    goods_item_db = await request.app.ctx.db.fetch_one(query=query)
    return goods_item_db


async def delete_goods_item_from_db(request, id: int):
    query = goods.delete().where(goods.c.id == id)
    deleted = await request.app.ctx.db.execute(query=query)
    goods_item = await get_goods_item_by_id(request, id)
    if goods_item is None:
        return response.json(
            {'message': f'goods item with id {id} was deleted successfully'}
        )


async def update_goods_item_db(request, id: int):
    values = {}
    if len(request.args) != 0:
        if 'title' in request.args:
            values['title'] = request.args['title'][0]
        if 'description' in request.args:
            values['description'] = request.args['description'][0]
        if 'price' in request.args:
            values['price'] = request.args['price'][0]
    if len(request.form) != 0:
        if 'title' in request.form:
            values['title'] = request.form['title'][0]
        if 'description' in request.form:
            values['description'] = request.form['description'][0]
        if 'price' in request.form:
            values['price'] = request.form['price'][0]
    if values:
        query = goods.update().where(goods.c.id == id).values(values)
        update = await request.app.ctx.db.execute(query)
        return response.json(
            {
                'message':
                f'properties {[key for key in values.keys()]}'
                f' were updated with values {[value for value in values.values()]}'
            }
        )
    return response.json({'message': 'No parameters to change'})
