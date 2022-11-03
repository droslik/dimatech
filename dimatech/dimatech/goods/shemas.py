from pydantic import BaseModel, Required


class GoodsItemCreate(BaseModel):
    title: str = Required
    description: str = Required
    price: int = Required


class GoodsItemUpdate(BaseModel):
    title: str
    description: str
    price: int
