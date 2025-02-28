from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os 
from dotenv import load_dotenv
# crear entorno -> python -m venv env
# activar entorno -> env\Scripts\activate
# instalar  -> pip install -r requirements.txt
# iniciar el servidor -> uvicorn app.main:app --reload

load_dotenv()
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory = "templates")
nombre = "marie"

# el icono predeterminado de la pestaña del navegador
favicon_path = 'favicon.ico'  # Adjust path to file

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)

# Rutas
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "nombre": nombre
    })

@app.get("/details", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("details.html", {
        "request": request,
        "nombre": nombre
    })

@app.get("/login", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("login.html", {
        "request": request,
        "nombre": nombre
    })

@app.get("/registre", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("registre.html", {
        "request": request,
        "nombre": nombre
    })