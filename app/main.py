from fastapi import FastAPI, APIRouter, Request, Body, Form, HTTPException, File, UploadFile, Depends, Query, Response, Header
from typing import Annotated
from typing import List
import json
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi_versioning import VersionedFastAPI, version

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from passlib.context import CryptContext
import jwt
#from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
#import app.models.crud 
from app.models.models import *
from app.models.crud import *
from app.models.database import get_db
# security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.database import fake_db, hash_password, verify_password
from app.auth import create_access_token_1, decode_access_token
from pydantic import BaseModel, Field
from datetime import timedelta

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


# Seguridad
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# Función para verificar la contraseña
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def compay_data(db: Session = Depends(get_db)):
    return obtener_Company(db, 1)
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

# Ruta para obtener el token
@api_v1.post("/token")
async def login_for_access_token(requests: Request, response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    #user = authenticate_user(form_data.username, form_data.password)
    user = search_user(db, form_data.username)
  
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")

    access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    access_token = create_access_token_1(data={"sub": user.password, "sub_":user.email}, expires_delta=access_token_expires)
    response.set_cookie(key="session", value=access_token, httponly=True)
    return {"access_token" : access_token, "token_type" : "bearer", "user" : user.id}

# Ruta protegida
@api_v1.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return {"message": f"Hola {username}, estás autenticado!"}
    except jwt:
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
class Cart(BaseModel):
    imagen: str
    titulo: str
    precio: float
    product_id: int
    cantidad: int 
    temp_date: datetime
    status: bool   
# finalir compra
@app.post("/buy")
async def buy(request: Request, carts: List[Cart],  db: Session = Depends(get_db)):

    print("Carts:", carts[0])
    #print([type(item) for item in carts[0]])
    #print(f"Carts decodificado: {carts[0]}, Tipo: {type(carts[0])}")
    session_token = request.cookies.get("session")
    usuario = decode_access_token(session_token)
    if not usuario:
        return RedirectResponse(url='/logout', status_code=303)
    user = search_user_cookie(db, usuario.get("sub_"), usuario.get("sub"))
    if user is None:
       return RedirectResponse(url='/logout', status_code=303)  
    id = user.id
    print("ID:", id)
    #carts = [json.loads(item) if isinstance(item, str) else item for item in carts]
    #for item in carts:
        #print(f"Item:", {item['product_id']})
    #items_db = [Cart(user_id=id, **item) for item in carts[0]] 
    #items_db = [Store_Cart(user_id=id, **json.loads(item)) if isinstance(item, str) else Store_Cart(user_id=id, **item.dict()) for item in carts[0]]
    #print("Items:", items_db) 
    items_db = [Store_Cart(user_id=id, **item) for item in carts]
    #carts = [Cart(**json.loads(item)) if isinstance(item, str) else item for item in carts]
    #items_db = [Cart(user_id=id, **item.dict()) for item in carts]
    #db.add_all(items_db)
    #db.commit()
    return RedirectResponse(url='/buy', status_code=303)
@app.get("/buy", response_class=HTMLResponse)
def login(request: Request,
                #carts: List = Body(None),
                company_data = Depends(compay_data)
                ):
    #print(carts)
    
    #print("Tipo de carts:", type(carts))
    #lista_carts = json.loads(carts)

    return templates.TemplateResponse("buy.html", {
        "request": request,
        "company": company_data,
        #"carts": carts
    })


# hacer el login
@app.get("/login", response_class=HTMLResponse)
async def login(request: Request, company_data = Depends(compay_data)):
    return templates.TemplateResponse("login.html", {
        "request": request,
        "company": company_data,
    })

# perfil de usuario
@app.post("/users")
async def edite_user(request: Request,
                    db: Session = Depends(get_db),
                    username: str = Form(...),
                    first_name: str = Form(...),
                    password: str = Form(...),
                    email: str = Form(...)
                    ): 
    session_token = request.cookies.get("session")
    usuario = decode_access_token(session_token)
    if not session_token:
        return RedirectResponse(url='/logout', status_code=303)
    user = search_user_cookie(db, usuario.get("sub_"), usuario.get("sub"))
    if user is None:
       return RedirectResponse(url='/logout', status_code=303)
    user.username = username 
    user.name = username
    user.first_name = ""
    user.last_name = first_name
    user.email = email
    user.password = hash_password(password)
    db.commit()   
    db.refresh(user) 
    return RedirectResponse(url='/users', status_code=303)

@app.get("/users", response_class=HTMLResponse)
async def read_users_me(request: Request,
                        company_data = Depends(compay_data),
                        db: Session = Depends(get_db),
                        ):
    session_token = request.cookies.get("session")
    usuario = decode_access_token(session_token)
    print(usuario.get("sub") , session_token)
    if not session_token:
        return RedirectResponse(url='/logout', status_code=303)

    user = search_user_cookie(db, usuario.get("sub_"), usuario.get("sub"))
    if user is None:
       return RedirectResponse(url='/logout', status_code=303)
    id = user.id
    cart_store = obtener_Cart(db, id)
    return templates.TemplateResponse("user.html", {
        "request": request,
        "company": company_data,
        "user": user,
        "cart_store": cart_store
    })

@app.post("/register")
async def register(request: Request,
                    db: Session = Depends(get_db),
                    username: str = Form(...),
                    password: str = Form(...),
                    email: str = Form(...),
                    last_name: str = Form(...)
                    ):    

    """Registra un usuario (almacena la contraseña hasheada)"""
    db_user = search_user(db, email)
    if db_user:
        return RedirectResponse(url='/register/error', status_code=303)
    hashed_password = hash_password(password)
    db_user = Users_User(   
            username = username,
            name = username,
            first_name = "",
            last_name = last_name,
            is_active = True,
            date_joined = datetime.now(),
            email = email,
            roll = "customer",
            active = True,
            password = hashed_password,
            company_id = 1
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return RedirectResponse(url='/login', status_code=303)

# registro de usuario
@app.get("/register", response_class=HTMLResponse)
@app.get("/register/{err}", response_class=HTMLResponse)
async def register(request: Request, err:str = None, company_data = Depends(compay_data)):
    if err == "error":
        error = "Usuario ya existe"  
    else:
        error = "" 
    return templates.TemplateResponse("registre.html", {
        "request": request,
        "company": company_data,
        "error": error
    })

@app.get("/logout")
def logout(response: Response, request: Request):
    #session_token = request.cookies.get("session")
    response.delete_cookie("token")
    response.delete_cookie("session")
    return RedirectResponse(url='/', status_code=303)


app.mount('/v1', api_v1)