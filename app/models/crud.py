from sqlalchemy.orm import Session
from app.models.models import *
import secrets
import string

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
def obtener_Cart_for(db : Session, user_id: int):
    return db.query(Store_Cart).filter(Store_Cart.user_id == user_id).all()

def obtener_Cart(db : Session, user_id: int, status: bool = True):
    return db.query(Store_Cart, Store_Products).join(Store_Cart, Store_Cart.product_id == Store_Products.id).filter(Store_Cart.user_id == user_id, Store_Cart.status == status).all()

# Compañia
def obtener_Company(db : Session, id : int):
    return db.query(Company_Company).filter(Company_Company.id == id).first()

# obtener facturas
def obtener_Invoices(db : Session, user_id: int):
    return db.query(Invoid).filter(Invoid.fk_user == user_id).order_by(Invoid.id.desc()).all()

# obtener sesiones
def obtener_Sessions(db : Session, session_key):
    print("recibido: ", session_key)
    return db.query(django_Session).filter(django_Session.session_key == session_key).first()



def generar_cadena_aleatoria(longitud=10):
    caracteres = string.ascii_letters + string.digits  # Letras mayúsculas, minúsculas y números
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))