from fastapi import FastAPI,HTTPException, Request, Form, Depends
from fastapi.responses import Response,RedirectResponse
from fastapi.middleware.cors import CORSMiddleware 
import logging
from datetime import datetime
from routers import users, services
from models.models import Contact
import os

from clases.send_email import EmailSender
from clases.logs import Log
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from typing import Annotated # Recomendado para tipado en Python 3.9+

from dotenv import load_dotenv

load_dotenv()
log = Log()

log.create_log("info","\n******************START APP*********************")
log.create_log("info","FastApi object instance")

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
    logging.info(" home: opening landing page")
    try:
        return RedirectResponse(url="/index", status_code= 307)
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
    print("entramos acá")
    EMAIL_HOST = os.environ.get('EMAIL_HOST')
    EMAIL_PORT = os.environ.get('EMAIL_PORT')
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

    logging.info(f"{EMAIL_HOST} {EMAIL_PORT} {EMAIL_HOST_USER} {EMAIL_HOST_PASSWORD}")

    send_email = EmailSender()
    send_email.configuracion(EMAIL_HOST,EMAIL_PORT,EMAIL_HOST_USER,EMAIL_HOST_PASSWORD)

    logging.info(f"Datos recibidos: \nNombre Completo={form_data.name } {form_data.last_name} teléfono= {form_data.phone} Email={form_data.email} Mensaje={form_data.message}")
    print(f"Datos recibidos: \nNombre Completo={form_data.name } {form_data.last_name}\nteléfono= {form_data.phone}\nEmail={form_data.email}\nMensaje={form_data.message}")

    # Ahora puedes guardar el objeto Pydantic en la DB, convertirlo a un modelo ORM, etc.
    send_email.envio_mensaje_sencillo(form_data.email, "Correo de prueba",f" {form_data.name}. Este es un correo de prueba, espero que todo funciones como lo espero.")
    
    template = templates.env.get_template('/email/email_automatic.html')
    context =  {
            'request':request,
            "message": "Datos recibidos, validados y procesados.",
            "name": form_data.name,
            "lastname":form_data.last_name, 
            "email": form_data.email,
        }
    # render() ejecuta el template y devuelve el HTML como una cadena
    html_content = template.render(context)
    
    send_email.envio_correo_html(EMAIL_HOST_USER,
                                 "Correo prueba html",
                                 html_content
                                )
    
    logging.info("Envio correo automático")
    

    return templates.TemplateResponse('thanks.html',
            {
                'request':request,
                'name': form_data.name,
                'last_name': form_data.last_name,
                'phone':form_data.phone,
                "email": form_data.email,
                "message": form_data.message
            }
        )