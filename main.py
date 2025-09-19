from fastapi import FastAPI, Depends
from models import Product
from database import session,engine
import database_models
from sqlalchemy.orm import Session

app = FastAPI()

# database_models.Base.metadata.create_all(bind=engine)


# @app.get("/")
# def greet():
#     return {"message": "Welcome to fastapi learning"}

# products = [
#     Product(id = 1, name = "Phone", description = "Amazing flagship mobile", price = 50000, quantity = 10),
#     Product(id = 2, name = "Laptop", description = "Great performance Laptop", price = 150000, quantity = 8),
#     Product(id = 3, name = "Accesories", description = "For both mobile and laptop", price = 5000, quantity = 100),
#     Product(id = 4, name = "Watch", description = "Most expensive watch", price = 200000, quantity = 2)
# ]

# def get_db():
#     db = session()
#     try:
#         yield db
#     finally:
#         db.close()

# def init_db():
#     db = session()
#     if(db.query(database_models.Product).count() == 0):
#         print("Adding initial data...")
#         for product in products:
#             db_product = database_models.Product(**product.model_dump())
#             db.add(db_product)
#         db.commit()
#     db.close()

# init_db()

# @app.get("/products")
# def get_all_products(db: Session = Depends(get_db)):
#     db_products = db.query(database_models.Product).all()
#     return {"products": db_products}

# @app.get("/searchproduct/{id}")
# def get_product_byId(id: int, db: Session = Depends(get_db) ):
#     db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
#     if db_product:
#         return {"Message": db_product}
#     return {"error": "product not found"}

# @app.post("/products")
# def add_products(product: Product, db: Session = Depends(get_db) ):
#     db.add(database_models.Product(**product.model_dump()))
#     db.commit()
#     return {"Message": "New product is added in db"}

# @app.put("/products")
# def update_products(id: int, product: Product, db: Session = Depends(get_db) ):
#     db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
#     if db_product:
#         db_product.name = product.name
#         db_product.description = product.description
#         db_product.price = product.price
#         db_product.quantity = product.quantity
#         db.commit()
#         return {"Message": "product is updated successfully"}
#     else:
#         return {"error": "no product found"}

# @app.delete("/products")
# def del_product(id: int, db: Session = Depends(get_db)):
#         db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
#         if db_product:
#             db.delete(db_product)
#             db.commit()
#             return {"Message": "Product deleted successfully"}
#         else:
#             return {"error": "No product found"}