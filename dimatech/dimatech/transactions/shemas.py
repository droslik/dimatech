from pydantic import BaseModel, Required


class PaymentWebhook(BaseModel):

    transaction_id: int = Required
    bill_id: int = Required
    user_id: int = Required
    amount: int = Required

