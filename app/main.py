import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas, database, auth


def create_app() -> FastAPI:
    app = FastAPI()

    from fastapi.security import OAuth2PasswordRequestForm
    @app.post("/token", response_model=schemas.Token)
    def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
        user = auth.authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = auth.create_access_token(
            data={"sub": user.email}
        )
        return {"access_token": access_token, "token_type": "bearer"}

    @app.post("/signup", status_code=201, description="Create a new user account")
    async def create_new_user(
            user: schemas.UserCreate, db: Session = Depends(database.get_db)
    ):
        db_user = crud.get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        return crud.create_user(db=db, user=user)

    @app.post("/signup-admin", status_code=201, description="Create a new admin account")
    async def create_new_admin(
            user: schemas.UserCreate, db: Session = Depends(database.get_db)
    ):
        db_user = crud.get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        return crud.create_admin(db=db, user=user)

    @app.post("/api/products/", response_model=schemas.Product)
    def create_product(
            product: schemas.ProductCreate,
            db: Session = Depends(database.get_db),
            current_user: models.User = Depends(auth.get_current_admin_user)
    ):
        print(f"Received product data: {product}")
        print(f"Current user: {current_user}")
        try:
            new_product = crud.create_product(db=db, product=product)
            print(f"Created product: {new_product}")
            return new_product
        except Exception as e:
            print(f"Error creating product: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
    @app.get("/api/products/{product_id}", response_model=schemas.Product)
    def read_product(product_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_admin_user)):
        db_product = crud.get_product(db, product_id=product_id)
        if db_product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return db_product

    @app.put("/api/products/{product_id}", response_model=schemas.Product)
    def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_admin_user)):
        db_product = crud.get_product(db, product_id=product_id)
        if db_product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return crud.update_product(db=db, product_id=product_id, product=product)

    @app.delete("/api/products/{product_id}", response_model=schemas.Product)
    def delete_product(product_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_admin_user)):
        db_product = crud.get_product(db, product_id=product_id)
        if db_product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return crud.delete_product(db=db, product_id=product_id)

    @app.get("/api/orders/", response_model=list[schemas.Order])
    def read_orders(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_admin_user)):
        return crud.get_orders(db)

    @app.get("/api/orders/{order_id}", response_model=schemas.Order)
    def read_order(order_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_admin_user)):
        db_order = crud.get_order(db, order_id=order_id)
        if db_order is None:
            raise HTTPException(status_code=404, detail="Order not found")
        return db_order

# customer

    @app.get("/api/products/", response_model=list[schemas.Product])
    def read_products(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_active_user)):
        return crud.get_products(db)

    @app.post("/api/orders/", response_model=schemas.Order)
    def create_order(order: schemas.OrderCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_active_user)):
        return crud.create_order(db=db, order=order)

    @app.get("/api/orders/{customer_id}", response_model=list[schemas.Order])
    def read_customer_orders(customer_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_active_user)):
        return crud.get_customer_orders(db, customer_id=customer_id)

    @app.get("/api/orders/{order_id}/status", response_model=str)
    def read_order_status(order_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_active_user)):
        db_order = crud.get_order(db, order_id=order_id)
        if db_order is None:
            raise HTTPException(status_code=404, detail="Order not found")
        return db_order.status

    return app

if __name__ == "__main__":
    uvicorn.run("app.main:create_app", host="127.0.0.1", port=8000, reload=True)