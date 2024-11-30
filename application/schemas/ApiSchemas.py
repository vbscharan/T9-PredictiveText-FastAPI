from pydantic import BaseModel,EmailStr
from typing import Optional

class ContactCreateSchema(BaseModel):
    name: str
    number: int

class ContactNameUpdateSchema(BaseModel):
    newname: str

class ContactNumberUpdateSchema(BaseModel):
    newnumber: int

class UserCreateSchema(BaseModel):
    username:str
    password:str
    email: Optional[EmailStr]=None

class UserLoginSchema(BaseModel):
    username:str
    password:str
    
class TokenSchema(BaseModel):
    accessToken:str
    tokenType:str

class TokenDataSchema(BaseModel):
    username:Optional[str]=None