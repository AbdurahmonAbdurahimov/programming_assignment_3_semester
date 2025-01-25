from sqlalchemy.orm import Session

from app import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        is_active=user.is_active,
        is_admin=user.is_admin,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_admin(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        is_active=user.is_active,
        is_admin=True,  # Always set is_admin to True for admins
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
#     return db_user
# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()
#
# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()
#
# def create_user(db: Session, user: schemas.UserCreate):
#     hashed_password = pwd_context.hash(user.password)
#     db_user = models.User(email=user.email, hashed_password=hashed_password, is_active=user.is_active, is_admin=user.is_admin)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# --- Product CRUD ---

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(name=product.name, description=product.description, price=product.price, category=product.category)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: schemas.ProductCreate):
    db_product = get_product(db, product_id=product_id)
    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.category = product.category
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id=product_id)
    db.delete(db_product)
    db.commit()
    return db_product

# --- Order CRUD ---

def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).offset(skip).limit(limit).all()

def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(customer_id=order.customer_id, order_date=order.order_date, status=order.status)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_customer_orders(db: Session, customer_id: int):
    return db.query(models.Order).filter(models.Order.customer_id == customer_id).all()


def create_order_detail(db: Session, order_detail: schemas.OrderDetailCreate):
    db_order_detail = models.OrderDetail(order_id=order_detail.order_id, product_id=order_detail.product_id, quantity=order_detail.quantity)
    db.add(db_order_detail)
    db.commit()
    db.refresh(db_order_detail)
    return db_order_detail