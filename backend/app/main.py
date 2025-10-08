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

logging.debug("****************************************************************************")
logging.debug("A INICIADO LA APLIACION")
logging.debug("Se instancia FastAPI")

app = FastAPI(
    title="Backend Interviniendo con Fé",
    description="API construida con Routers, Middleware y Eventos. Para toda la funcionalidad de la página para Mariana Suarez, interviniendo con fe. Esperemos que todo salga super bien",
    version="2.0.0",
    )
logging.info("Esta instancia, nos permite usar el objeto FastAPI, para configurar el servidors")

# Configuración de CORS (Permitir que el frontend acceda a la API)
origins = [
    "http://localhost:3000",  
    "http://localhost:8000", 
    "http://localhost:80001", 
]
logging.info(f"Se han configurado los siguiente CORS {origins}")

logging.debug("Se configuran los origenes y los métodos habilitados")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,     # Dominios permitidos (o ["*"] para permitir todos)
    allow_credentials=True,    # Permitir cookies y encabezados de autorización
    allow_methods=["*"],       # Permitir todos los métodos (GET, POST, PUT, DELETE)
    allow_headers=["*"],       # Permitir todos los encabezados
)
logging.info("Se han configurado los origenes y los métodos habilitados")

# Routers

app.include_router(users.router)    
app.include_router(services.router) 

# EndPoints
@app.get("/", tags=["Home"])
async def home():
    """Verifica si el servidor está activo."""
    logging.info("Se ingresa a la ruta home, para verificar conexión")
    try:
        return {
            "status": "ok", 
            "service": "fastapi_backend",
            "message":"La aplicación está funcionando correctamente",
            "developer":"Camilo Cañaverl (cc_dev)",
            "company":"Interviniendo con Fé"
        }
    except:
        raise HTTPException(status_code=404, detail="Página no encontrada")
