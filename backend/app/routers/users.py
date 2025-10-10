from fastapi import APIRouter
from models.models import User
from datetime import datetime
import logging

fecha_actual = datetime.now().strftime('%m-%d-%G')

logging.basicConfig(
    filename=f'logs_{fecha_actual}.log', 
    filemode='a',
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

router =  APIRouter(
    prefix="/users",
    tags=["users"],
)

fake_db=[
    {
        "id":0,
        "name":"string",
        "last_name":"String",
        "document":"String",
        "email":"String",
        "coment":"String"
    },
    {
        "id":1,
        "name":"string",
        "last_name":"String",
        "document":"String",
        "email":"String",
        "coment":"String"
    },{
        "id":2,
        "name":"string",
        "last_name":"String",
        "document":"String",
        "email":"String",
        "coment":"String"
    }
]

@router.get('/')
async def get_all_users():
    logging.info("Se ha ingresado al endponti /users/")
    return fake_db

@router.post('/')
async def get_all_users(user:User):
    logging.info(f"add user {user}")
    fake_db.append(user)
    return fake_db