from fastapi import FastAPI, Request, Form, HTTPException, Depends, Response
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import secrets
import jwt
from datetime import datetime, timedelta,  timezone
from sqlalchemy.orm import Session
from app.models.models import *
from app.models.crud import *
from app.auth import *
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


# Seguridad
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Función para obtener el compañia
def compay_data(db: Session = Depends(get_db)):
    return obtener_Company(db, 1)

# comprobar la cookie y obtener el id del usuario
def compro_cookie_id(request, db):    
   
    try:
        usuario = decode_access_token(request.cookies.get("session"))
        if not usuario:
            user = "error"
        print("Usuario -----")
        print(usuario)
        user = search_user_cookie(db, usuario.get("sub_"), usuario.get("sub_b"))
        if user is None:
            print("User ------ ")
            user = "error"
    except Exception as e:
        print("Errror ------ ")
        print(f"Error decoding token: {e}")
        user = "error"
    
    
    return user


# Ruta para obtener el token
@api_v1.post("/token")
async def login_for_access_token(response: Response,
                                requests: Request,
                                form_data: OAuth2PasswordRequestForm = Depends(),
                                db: Session = Depends(get_db)):
    #user = authenticate_user(form_data.username, form_data.password)
    user = search_user(db, form_data.username)
    print(user)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")
    session_key = secrets.token_urlsafe(30)[:40]
    access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    access_token = create_access_token_1(data={"sub": session_key, "sub_":user.email, "sub_b":user.password}, expires_delta=access_token_expires)
    response.set_cookie(key="session", value=access_token)
    now = datetime.utcnow()
    delta = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    new_time = now + delta
    
    session_django = django_Session(session_key=session_key, session_data=access_token, expire_date=new_time.isoformat())
    db.add(session_django)
    db.commit()
    response.headers["Authorization"] = f"Bearer {access_token}"
    return {"access_token" : access_token, "token_type" : "bearer", "user" : user.id}

# Ruta protegida
@api_v1.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        username = payload.get("sub_")
        print(username)
        #if username is None:
            #raise HTTPException(status_code=401, detail="Token inválido")
        return {"message": f"Hola {username}, estás autenticado!"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="El token ha expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
    


# Rutas
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, company_data = Depends(compay_data), db: Session = Depends(get_db) ):
    all_products = obtener_Products(db)
    return templates.TemplateResponse(request, "index.html", {
        "request": request,
        "company": company_data,
        "all_products": all_products
    })

# Detalles de producto
@app.get("/details/{id}", response_class=HTMLResponse)
async def detalails(request: Request, id: int, company_data = Depends(compay_data), db: Session = Depends(get_db)):
    detalails = obtener_Product_por_id(db, id)
    return templates.TemplateResponse(request, "details.html", {
        "request": request,
        "company": company_data,
        "detalails": detalails
    })

# procesar pago
@app.get("/pay",  response_class=HTMLResponse)
async def pay(request: Request, db: Session = Depends(get_db), company_data = Depends(compay_data),):
    usuario = decode_access_token(request.cookies.get("session"))
    if not usuario:
        return RedirectResponse(url='/logout', status_code=303) 
    session_b = obtener_Sessions(db, usuario.get("sub"))
    if session_b and (session_b.expire_date) > datetime.now(timezone.utc).replace(tzinfo=timezone.utc):
        user = compro_cookie_id(request, db)
        print(user.id)
        if user == "error":
            return RedirectResponse(url='/logout', status_code=303)
        # todos los elemento
        carts = obtener_Cart_for(db, user.id)
        if not carts:
            raise HTTPException(status_code=400, detail="No hay productos en el carrito")

        total_neto = sum(cart.precio for cart in carts)
        create_invoid = Invoid(
            date=datetime.now(),
            payment_form="efectivo",
            neto= total_neto,
            fk_type=1,
            fk_user=user.id,
            fk_company=company_data.id
        )
        db.add(create_invoid)
        db.commit()
        db.refresh(create_invoid)
        
        for cart_item in carts:
            create_invoid_items = Invoid_Items(
                invoice_id=create_invoid.id,
                product_id= cart_item.product_id,
                quantity=cart_item.cantidad,
                price=cart_item.precio
            )
            db.add(create_invoid_items)
            # borramos los temporales
            db.delete(cart_item)  
            db.commit()
        db.commit()
        
        return templates.TemplateResponse(request, "finish.html", {
            "request": request,
            "company": company_data,
            "carts": carts
        })
    else:
        return RedirectResponse(url='/logout', status_code=303)
# procesar compra
@api_v1.post("/buy")
async def buy(request: Request, db: Session = Depends(get_db)):
    data = await request.json()

    user = compro_cookie_id(request, db)
    print(user.id)
    if user == "error":
        return RedirectResponse(url='/logout', status_code=303)
    carrito = data.get('carrito', [])
    for item in carrito:
        new_cart_item = Store_Cart(
            user_id=user.id,
            product_id=item['product_id'],
            cantidad=item['cantidad'],
            precio=item['precio'],
            temp_date=datetime.now(),
            status=False 
        )
        db.add(new_cart_item)
    db.commit()
    return RedirectResponse(url='/', status_code=303)
# factura
@app.get("/invoice", response_class=HTMLResponse)
async def invoice(request: Request, db: Session = Depends(get_db), company_data = Depends(compay_data)):
    usuario = decode_access_token(request.cookies.get("session"))
    if not usuario:
        return RedirectResponse(url='/logout', status_code=303) 
    session_b = obtener_Sessions(db, usuario.get("sub"))
    if session_b and (session_b.expire_date) > datetime.now(timezone.utc).replace(tzinfo=timezone.utc):
        user = compro_cookie_id(request, db)
        if user == "error":
            return RedirectResponse(url='/logout', status_code=303)
        #invoid = obtener_Invoid(db, user.id)
        carts = obtener_Cart(db, user.id, False)
        return templates.TemplateResponse(request, "invoice.html", {
            "request": request,
            "company": company_data,
            "carts": carts
            #"invoid": invoid
        })
    else:
        return RedirectResponse(url='/logout', status_code=303)
# finalir compras
@app.get("/cart", response_class=HTMLResponse)
def login(request: Request,
                company_data = Depends(compay_data),
                db: Session = Depends(get_db)
                ):
    usuario = decode_access_token(request.cookies.get("session"))
    if not usuario:
        return RedirectResponse(url='/logout', status_code=303) 
    session_b = obtener_Sessions(db, usuario.get("sub"))
    if session_b and (session_b.expire_date) > datetime.now(timezone.utc).replace(tzinfo=timezone.utc):
        user = compro_cookie_id(request, db)
        if user == "error":
            return RedirectResponse(url='/logout', status_code=303)
        carts = obtener_Cart(db, user.id, False)
        print(carts)
        return templates.TemplateResponse(request, "buy.html", {
            "request": request,
            "company": company_data,
            "carts": carts
        })
    else:
        return RedirectResponse(url='/register', status_code=303)

# hacer el login
@app.get("/login", response_class=HTMLResponse)
async def login(request: Request, company_data = Depends(compay_data)):
    return templates.TemplateResponse(request, "login.html", {
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

    user = compro_cookie_id(request, db)
    if user == "error":
        return RedirectResponse(url='/logout', status_code=303)
    user.username = username 
    user.name = username
    user.first_name = ""
    user.last_name = first_name
    user.email = email
    user.password = hash_password(password)
    db.commit()   
    db.refresh(user) 
    
    return RedirectResponse(url='/logout', status_code=303)

@app.get("/users", response_class=HTMLResponse)
async def read_users_me(request: Request,
                        company_data = Depends(compay_data),
                        db: Session = Depends(get_db),
                        ):
    usuario = decode_access_token(request.cookies.get("session"))
    if not usuario:
        return RedirectResponse(url='/logout', status_code=303) 
    session_b = obtener_Sessions(db, usuario.get("sub"))
    if session_b and (session_b.expire_date) > datetime.now(timezone.utc).replace(tzinfo=timezone.utc):
        user = compro_cookie_id(request, db)
        if user == "error":
            return RedirectResponse(url='/logout', status_code=303)
        cart_store = obtener_Cart(db, user.id)
        invoices = obtener_Invoices(db, user.id)
        return templates.TemplateResponse(request, "user.html", {
            "request": request,
            "company": company_data,
            "user": user,
            "cart_store": cart_store,
            "invoices": invoices
        })
    else:
        return RedirectResponse(url='/logout', status_code=303)

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
    return templates.TemplateResponse(request, "registre.html", {
        "request": request,
        "company": company_data,
        "error": error
    })



@app.get("/logout")
async def logout(response: Response, request: Request, db: Session = Depends(get_db),):
    print("cerrando sesion")
    usuario = decode_access_token(request.cookies.get("session"))
    #session = db.query(obtener_Sessions).filter_by(session_key=usuario.get("sub")).first()
    session_b = obtener_Sessions(db, usuario.get("sub"))
    if session_b:
        db.delete(session_b)  
        db.commit()
    # Eliminar cookies asegurando que afectan toda la app
    response.delete_cookie(key="token", path="/")
    response.set_cookie(key="session", value="")
    response.delete_cookie(key="session", path="/")
    return RedirectResponse(url='/', status_code=303)

from xhtml2pdf import pisa
@app.get("/generate-invoice")
async def generate_pdf(request: Request,
                        company_data = Depends(compay_data),
                        db: Session = Depends(get_db),):
    usuario = decode_access_token(request.cookies.get("session"))
    session_b = obtener_Sessions(db, usuario.get("sub"))
    if session_b and (session_b.expire_date) > datetime.now(timezone.utc).replace(tzinfo=timezone.utc):
        user = compro_cookie_id(request, db)
        if user == "error":
            return RedirectResponse(url='/logout', status_code=303)
        print(user.id)
        # Definir el HTML
        html_content = """
        <html>
        <head>
            <title>Ejemplo de PDF</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; }
                h1 { color: blue; }
            </style>
        </head>
        <body>
            <h1>Hola {{ user.id }}, {% user.id %} este es un PDF generado con FastAPI y WeasyPrint</h1>
            <p>Este PDF se ha generado a partir de HTML.</p>
        </body>
        </html>
        """

        with open('templates/template.html', 'r', encoding='utf-8') as source_html:
            html_content = source_html.read()
        
        source_html.close() 
        html_content = html_content.replace("clienteA", str(user.id))
        pdf_path = f"{generar_cadena_aleatoria()}.pdf"
        pdf = pisa.CreatePDF(html_content)

        response = Response(content=pdf.dest.getvalue(), media_type="application/pdf")
        response.headers["Content-Disposition"] = f"attachment; filename={pdf_path}"
        return response
        #return FileResponse(pdf_path, media_type="application/pdf", filename=pdf_path)
    else:
        return RedirectResponse(url='/logout', status_code=303)
    
    
app.mount('/v1', api_v1)