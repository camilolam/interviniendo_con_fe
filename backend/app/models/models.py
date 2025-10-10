from pydantic import BaseModel

# usuarios
class User(BaseModel):
    id:int
    name:str
    last_name:str
    document:str
    email:str
    coment:str

class Service(BaseModel):
    id:int
    icon:str 
    name:str

class Testimonial(BaseModel):
    id:int 
    coment:str
    img:str
    name:str
    title:str