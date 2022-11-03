from transactions.handlers import payment, get_own_transactions

transactions_urls = [
    {'uri': '/payment/webhook/', 'handler': payment, 'methods': ['POST']},
    {'uri': '/transactions/', 'handler': get_own_transactions, 'methods': ['GET']}
]
