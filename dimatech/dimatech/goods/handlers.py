from sanic import response
from sanic_ext import openapi
from goods.shemas import GoodsItemCreate
from permissions import admin_permission
from goods.crud import (
    get_goods_item_by_id,
    update_goods_item_db,
    delete_goods_item_from_db
)
from goods.services import create_goods_service, buy_goods_item
from models import goods


# url /goods/
async def view_goods(request):
    if request.method == 'GET':
        query = goods.select()
        goods_db = await request.app.ctx.db.fetch_all(query=query)
        return response.json({'goods': [{**good_db} for good_db in goods_db]})


# url: /goods/create/
@openapi.body(GoodsItemCreate)
@openapi.parameter('token', str, 'header', required=True)
@admin_permission
async def create_goods(request):
    return await create_goods_service(request)


# url: /goods/<id>/
async def get_goods_item(request, id: int):
    goods_item_db = await get_goods_item_by_id(request, id)
    if goods_item_db:
        return response.json({'goods_item': {**goods_item_db}})
    return response.json({'message': f'item with id:{id} was not found',
                          'status_code': 404})


# url: /goods/<id>/delete/
@openapi.parameter('token', str, 'header', required=True)
@admin_permission
async def delete_goods_item(request, id: int):
    goods_item_db = await get_goods_item_by_id(request, id)
    if goods_item_db:
        return await delete_goods_item_from_db(request, id)
    return response.json({'message': f'item with id:{id} was not found',
                          'status_code': 404})


# url: /goods/<id>/update/
@openapi.parameter('token', str, 'header', required=True)
@openapi.parameter('title', str)
@openapi.parameter('description', str)
@openapi.parameter('price', int)
@admin_permission
async def update_goods_item(request, id: int):
    goods_item_db = await get_goods_item_by_id(request, id)
    if goods_item_db:
        return await update_goods_item_db(request, id)
    return response.json({'message': f'item with id:{id} was not found',
                          'status_code': 404})


# url: /goods/<id>/buy/
@openapi.parameter('token', str, 'header', required=True)
async def buy_goods(request, id: int):
    return await buy_goods_item(request, id)
