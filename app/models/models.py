from sqlalchemy import Column, Integer, String, Float, Boolean, TIMESTAMP, ForeignKey, Text, BINARY, LargeBinary

try:
    from sqlalchemy.orm import declarative_base  # SQLAlchemy 2.x
except ImportError:
    from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Users_User(Base):
    __tablename__ = "users_user"

    id = Column(Integer, primary_key=True, index=True)
    is_superuser = Column(Boolean , default=False)
    is_staff = Column(Boolean , default=False)
    username = Column(String, index=True)
    name = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    is_active = Column(Boolean, default=True)
    date_joined = Column(TIMESTAMP)
    email = Column(String, unique=True, index=True)
    roll = Column(String)
    active = Column(Boolean, default=True)
    password = Column(String)
    company_id = Column(Integer)

class Store_Products(Base):
    __tablename__ = "store_products"

    id = Column(Integer, primary_key=True, index=True)
    iva = Column(Float, index=True)
    category = Column(String)
    name = Column(String)
    description = Column(String)
    amount = Column(Integer)
    image = Column(String)
    net_price = Column(Float)
    fk_company = Column(Integer)
    fk_type = Column(Integer)
    stock_inicial = Column(Integer)
    stock = Column(Integer)

# Compañia
class Company_Company(Base):
    __tablename__ = "company_company"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    mail = Column(String)
    phone = Column(String)
    direction = Column(String)
    cif = Column(String)

# cesta
class Store_Cart(Base):
    __tablename__ = "basket_temp_items"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    product_id = Column(Integer)
    cantidad = Column(Integer)
    precio = Column(Float)
    temp_date = Column(TIMESTAMP)
    status = Column(Boolean, default=True)

class Invoid(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(TIMESTAMP)
    payment_form = Column(String)
    neto = Column(Float)
    fk_type = Column(Integer)
    fk_user = Column(Integer)
    fk_company = Column(Integer)

class Invoid_Items(Base):
    __tablename__ = "invoice_items"
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer)
    product_id = Column(Integer)
    quantity = Column(Integer)
    price = Column(Float)

class django_Session(Base):
    __tablename__ = "django_session"
    session_key =   Column(String(40), primary_key=True)
    session_data = Column(String)
    expire_date = Column(TIMESTAMP) 