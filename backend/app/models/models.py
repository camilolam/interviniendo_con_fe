from pydantic import BaseModel, Field, validator 
from typing import Annotated 
from fastapi import Form

# usuarios
class User(BaseModel):
    id:int 
    name:str = Field(min_length = 5, max_length = 15)
    last_name:str = Field(min_length = 5, max_length = 15)
    document:str = Field(min_length = 8, max_length = 15)
    email:str = Field(min_length = 5, max_length = 15)
    coment:str = Field(max_length = 40)

class Service(BaseModel):
    id:int
    icon:str = Field(min_length = 5)
    name:str = Field(min_length = 5,  max_length = 15) 

class Testimonial(BaseModel):
    id:int 
    coment:str = Field(max_length = 30) 
    img:str
    name:str = Field(min_length = 5,  max_length = 15) 
    title:str = Field(min_length = 5,  max_length = 40) 

class Contact(BaseModel):
    name: Annotated[str, Field(min_length=2)]
    last_name: Annotated[str, Field(min_length=2)]
    phone: Annotated[str, Field(min_length=4)]
    email: Annotated[str, Field()]
    message: Annotated[str, Field(max_length=500)]

    @classmethod
    def as_form(
        cls,
        # La clave es usar Form() para cada parámetro de este método
        name: Annotated[str, Form()],
        last_name: Annotated[str, Form()],
        phone: Annotated[str, Form()],
        email: Annotated[str, Form()],
        message: Annotated[str, Form()]
    ):
        """Método de fábrica que crea una instancia de ContactForm a partir de datos de Form."""
        # Se retorna la instancia del modelo, mapeando los argumentos a sus campos
        return cls(
            name=name ,
            last_name=last_name,
            phone=phone,
            email=email,
            message=message
        )