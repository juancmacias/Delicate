from sqlalchemy.orm import Session
from app.models.models import *

# Usuarios
def obtener_Users(db : Session):
    return db.query(Users_User).all()
# obtener usuario por id
def obtener_User_por_id(db: Session, user_id: int):
    return db.query(Users_User).filter(Users_User.id == user_id).first()
def search_user(db: Session, email: str):
    return db.query(Users_User).filter(Users_User.email == email, Users_User.roll == 'customer').first() 
def search_user_cookie(db: Session, email: str, password: str):
    return db.query(Users_User).filter(Users_User.email == email, Users_User.password == password).first() 

# Productos
def obtener_Products(db : Session):
    return db.query(Store_Products).all()

# obtener producto por id   
def obtener_Product_por_id(db: Session, product_id: int):
    return db.query(Store_Products).filter(Store_Products.id == product_id).first()

#obtener lista de la compra
def obtener_Cart(db : Session, user_id: int):
    return db.query(Store_Cart).filter(Store_Cart.user_id == user_id).all()

# Compañia
def obtener_Company(db : Session, id : int):
    return db.query(Company_Company).filter(Company_Company.id == id).first()
