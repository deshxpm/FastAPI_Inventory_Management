from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str


class ItemBase(BaseModel):
    name: str
    description: str = None
    price: int

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    # Inherits all fields from ItemBase
    pass

class ItemResponse(ItemBase):
    id: int

    class Config:
        from_attributes = True
