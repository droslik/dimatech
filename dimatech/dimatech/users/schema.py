from pydantic import BaseModel, Required


class UserBase(BaseModel):
    username: str = Required

    class Config:
        orm_mode = True


class UserSchema(UserBase):
    password: str = Required

