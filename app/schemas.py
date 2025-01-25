from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    is_active: bool
    is_admin: bool

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    class Config:
        from_attributes = True  # Updated from 'orm_mode'

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    category: str

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    class Config:
        from_attributes = True  # Updated from 'orm_mode'


class OrderBase(BaseModel):
    customer_id: int
    order_date: str
    status: str

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    class Config:
        from_attributes = True  # Updated from 'orm_mode'

class OrderDetailBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int

class OrderDetailCreate(OrderDetailBase):
    pass

class OrderDetail(OrderDetailBase):
    id: int
    class Config:
        from_attributes = True  # Updated from 'orm_mode'

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None