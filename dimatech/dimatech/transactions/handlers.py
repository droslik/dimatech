from sanic import response
from sanic_ext import openapi
from transactions.crud import get_transactions_by_user_id
from transactions.services import effect_payment
from transactions.shemas import PaymentWebhook
from users.services import get_user_id_by_token


# url /payment/webhook/
@openapi.body(PaymentWebhook)
async def payment(request):
    result = await effect_payment(request)
    if isinstance(result, str):
        return response.json({'message': result})
    return response.json({'transaction': {**result}})


# /own_transactions/
@openapi.parameter('token', str, 'header', required=True)
async def get_own_transactions(request):
    user_id = await get_user_id_by_token(request)
    if isinstance(user_id, int):
        transactions = await get_transactions_by_user_id(request, user_id)
        return response.json({'transactions': [{**transaction} for transaction in transactions]})
    return response.json({'message': user_id})
