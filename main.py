from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os 
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
templates = Jinja2Templates(directory = "templates")
nombre = "marie"

@app.get("/")
async def read_root(request: Request):
    return HTMLResponse("Bienvenido a mi Web")
    #return HTMLResponse(templates.TemplateResponse(
        #request = request, name = "pagina.html", context = {"id": nombre}
    #))
