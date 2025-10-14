from fastapi import FastAPI,HTTPException, Request, Form, Depends
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware 
import logging
from datetime import datetime
from routers import users, services
from models.models import Contact
import os

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from typing import Annotated # Recomendado para tipado en Python 3.9+

fecha_actual = datetime.now().strftime('%m-%d-%G')

logging.basicConfig(
    filename=f'logs_{fecha_actual}.log', 
    filemode='a',
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.debug("")
logging.debug("\n******************START APP*********************")
logging.debug("FastApi object instance")

app = FastAPI(
    title="Backend Interviniendo con Fé",
    description="API for backend, of interviniendo con fe.",
    version="2.0.0",
    )

static_path = os.path.join(os.path.dirname(__file__),'static/')
templates_path = os.path.join(os.path.dirname(__file__),'templates/')

app.mount('/static',StaticFiles(directory=static_path),'static')
templates = Jinja2Templates(directory=templates_path)

# Configuración de CORS (Permitir que el frontend acceda a la API)
origins = [
    "http://localhost:3000",  
    "http://localhost:8000", 
    "http://localhost:80001", 
]
logging.info(f"CORS: {origins}")

logging.debug("Se configuran los origenes y los métodos habilitados")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,     # Dominios permitidos (o ["*"] para permitir todos)
    allow_credentials=True,    # Permitir cookies y encabezados de autorización
    allow_methods=["*"],       # Permitir todos los métodos (GET, POST, PUT, DELETE)
    allow_headers=["*"],       # Permitir todos los encabezados
)

# Routers
logging.debug("Add routers users, services")
app.include_router(users.router)    
app.include_router(services.router) 

fake_db=[
        {
            "name":"string",
            "phone":"String",
            "email":"String",
            "message":"String"
        },
    ]


logging.debug("End configuration") 
# EndPoints
@app.get("/", tags=["Home"])
async def home():
    """varify if server is active"""
    logging.info(" home: verify server")
    try:
        return {
            "status": "ok", 
            "service": "fastapi_backend",
            "message":"succes",
            "developer":"Camilo Cañaveral (cc_dev)",
            "company":"Interviniendo con Fé"
        }
    except:
        raise HTTPException(status_code=404, detail="Página no encontrada")
    
@app.get("/index", tags=["Home"])
async def home(request:Request):
    return templates.TemplateResponse('index.html',
            {
                'request':request,
                'message':'Bienvenido a esta página',

            }
        )

@app.post("/contact_form", tags=["Home"])
async def submit_form(request:Request, form_data: Contact = Depends(Contact.as_form)):

    print(f"Datos recibidos: Nombre={form_data.name }, Email={form_data.email}")

    # Ahora puedes guardar el objeto Pydantic en la DB, convertirlo a un modelo ORM, etc.
    
    res =  {
        "mensaje": "Datos recibidos, validados y procesados.",
        "nombre": form_data.name,
        "email": form_data.email,
        "largo_mensaje": len(form_data.message)
    }

    return templates.TemplateResponse('thanks.html',
            {
                'request':request,
                'name': form_data.name,
                'phone':form_data.phone,
                "email": form_data.email,
                "message": form_data.message
            }
        )