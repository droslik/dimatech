from Crypto.Hash import SHA1
from settings import Settings
from transactions.crud import create_transaction
from users.crud import (
    get_user_by_id,
    get_user_accounts_from_db,
    create_user_account,
    update_account_balance_transaction
)


async def effect_payment(request):
    webhook = await sign_transaction(request)
    result = await payment_processing(request, webhook)
    return result


async def sign_transaction(request):
    transaction_id = request.json['transaction_id']
    bill_id = request.json['bill_id']
    user_id = request.json['user_id']
    amount = request.json['amount']
    signature = SHA1.new()
    signature.update(
        f'{Settings.PRIVATE_KEY}:{transaction_id}:{user_id}:{bill_id}:{amount}'
        .encode()
    )
    signature = signature.hexdigest()
    print(signature)
    webhook = {'signature': signature,
               'transaction_id': transaction_id,
               'bill_id': bill_id,
               'user_id': user_id,
               'amount': amount}
    return webhook


async def payment_processing(request, webhook):
    user_id = webhook['user_id']
    bill_id = webhook['bill_id']
    amount = webhook['amount']
    user = await get_user_by_id(request, user_id)
    if user is None:
        message = 'user not found'
        return message
    accounts = await get_user_accounts_from_db(request, user_id)
    if accounts:
        bill_ids = [account['bill_id'] for account in accounts]
        if bill_id in bill_ids:
            index_bill = bill_ids.index(bill_id)
            new_balance = accounts[index_bill]['balance'] + amount
            await update_account_balance_transaction(
                request, bill_id, new_balance
            )
        new_account = await create_user_account(request, user_id)
        bill_id = new_account['bill_id']
        await update_account_balance_transaction(request, bill_id, amount)
    else:
        new_account = await create_user_account(request, user_id)
        bill_id = new_account['bill_id']
        await update_account_balance_transaction(request, bill_id, amount)
    transaction = await create_transaction(request, user_id, bill_id, amount)
    if transaction:
        return transaction
