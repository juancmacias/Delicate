from fastapi import FastAPI, APIRouter, Request, Form, HTTPException, status, File, UploadFile, Depends, Cookie, Response
from typing import Annotated
import psycopg2
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi_versioning import VersionedFastAPI, version
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
#import app.models.crud 
from app.models.crud import obtener_Company, obtener_Products, obtener_Product_por_id
from app.models.database import get_db


import os 
from dotenv import load_dotenv

# crear entorno -> python -m venv env
# activar entorno -> env\Scripts\activate
# instalar  -> pip install -r requirements.txt
# iniciar el servidor -> uvicorn app.main:app --reload <<<<----- nop
# ejecutar el servidor -> python main.py
# para leer el .env

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)
app = FastAPI(
    title="API de market place",
    description="Esta api maneja los elementos para mostrar los productos de la tienda con FastAPI",
    version="0.1",  
    redoc_url="/docs")
# Versión de la API
api_v1 = FastAPI(title="API de login y validación de token",
    description="Esta api maneja del login para la validación de ususarios con FastAPI",
    version="v1",
    redoc_url="/docs")

api_v1.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory = "templates")
nombre = "marie"
# Configuración
#SECRET_KEY = "secret_key_123"
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# Base de datos simulada
# secret
fake_users_db = {
    "usuario": {
        "username": "usuario",
        "full_name": "Usuario Ejemplo",
        "email": "usuario@example.com",
        #ashed_password": "$2b$12$Wz5HjizHUpbQ2JG2fPJL0uQ0csqx9HaWyDapzswJhXJQZp0qfJgPK",  # Contraseña: "1234"
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}
# Seguridad
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# Función para verificar la contraseña
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Función para obtener usuario
def get_user(db, username: str):
    user = db.get(username)
    if user:
        return user

# Función para autenticar usuario
def authenticate_user(username: str, password: str):
    user = get_user(fake_users_db, username)
    if not user or not verify_password(password, user["hashed_password"]):
        return False
    return user

# Función para generar el token JWT
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def compay_data(db: Session = Depends(get_db)):
    return obtener_Company(db, 1)

# Ruta para obtener el token
@api_v1.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer"}

# Ruta protegida
@api_v1.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return {"message": f"Hola {username}, estás autenticado!"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    

# el icono predeterminado de la pestaña del navegador
favicon_path = 'favicon.ico'  # Adjust path to file

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)

# Rutas
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, company_data = Depends(compay_data), db: Session = Depends(get_db) ):
    all_products = obtener_Products(db)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "company": company_data,
        "all_products": all_products
    })

# Detalles de producto
@app.get("/details/{id}", response_class=HTMLResponse)
async def detalails(request: Request, id: int, company_data = Depends(compay_data), db: Session = Depends(get_db)):
    detalails = obtener_Product_por_id(db, id)
    return templates.TemplateResponse("details.html", {
        "request": request,
        "company": company_data,
        "detalails": detalails
    })

# hacer el login
@app.get("/login", response_class=HTMLResponse)
async def login(request: Request, company_data = Depends(compay_data)):
        return templates.TemplateResponse("login.html", {
        "request": request,
        "company": company_data
    })

# perfil de usuario
@app.get("/users", response_class=HTMLResponse)
async def read_users_me(request: Request, company_data = Depends(compay_data)):
    return templates.TemplateResponse("user.html", {
        "request": request,
        "company": company_data
    })

# registro de usuario
@app.get("/registre", response_class=HTMLResponse)
async def register(request: Request, company_data = Depends(compay_data)):
    return templates.TemplateResponse("registre.html", {
        "request": request,
        "nombre": company_data
    })



app.mount('/v1', api_v1)