from fastapi import status,HTTPException,APIRouter
from application.schemas.ApiSchemas import *
from application import PasswordHashAndVerify
from application.controllers.UserController import *
from application import main
from application.models.DatabaseConnection import SingletonDatabaseConnection
from application import oauth2

router=APIRouter(tags=['User'])

user=User()

db=SingletonDatabaseConnection.getInstance().db

@router.post("/users",status_code=status.HTTP_201_CREATED)
def createUser(payload:UserCreateSchema):
    #Hash the user password

    payload.password=PasswordHashAndVerify.hash(payload.password)
    result=user.createUser(db.getDatabaseConnection(),db.getDatabaseCursor(),payload)
    if result=='Username already exists':
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="'"+payload.username+"' username is already taken, try another one")
    return "'"+payload.username+"' is created"