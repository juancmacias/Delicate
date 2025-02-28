from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
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

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("pagina.html", {
        "request": request,
        "nombre": nombre
    })

