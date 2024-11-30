from fastapi import APIRouter,HTTPException,status
from application.models.DatabaseConnection import SingletonDatabaseConnection
from application.schemas import ApiSchemas
from application import PasswordHashAndVerify
from application import oauth2

router=APIRouter(tags=['Authentication'])

db=SingletonDatabaseConnection.getInstance().db
cursor=db.getDatabaseCursor()
conn=db.getDatabaseConnection()

@router.post("/login")
def userLogin(userCreds:ApiSchemas.UserLoginSchema):
    cursor.execute("SELECT * FROM users WHERE username=(%s)",(userCreds.username,))
    result=cursor.fetchone()
    if result is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Credentials")
    if not PasswordHashAndVerify.verify(userCreds.password,result['password']):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Credentials")
    jsonWebToken=oauth2.createJWT({"username":userCreds.username})
    return {"token":jsonWebToken, "token_type":"bearer"}

