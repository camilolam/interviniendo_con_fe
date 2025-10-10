from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware 
import logging
from datetime import datetime
from routers import users, services
#from models.models import User, Service, Testimonial

fecha_actual = datetime.now().strftime('%m-%d-%G')

logging.basicConfig(
    filename=f'logs_{fecha_actual}.log', 
    filemode='a',
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.debug("")
logging.debug("START APP \n")
logging.debug("FastApi object instance")

app = FastAPI(
    title="Backend Interviniendo con Fé",
    description="API for backend, of interviniendo con fe.",
    version="2.0.0",
    )

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
