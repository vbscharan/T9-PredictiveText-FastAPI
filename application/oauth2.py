from jose import JWTError,jwt
from datetime import datetime,timedelta,timezone
from application.schemas import ApiSchemas
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer

#oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")
#secretKey
#algorithm-HS256
#expiration time

secretKey="hadkciutavf828r712837r068ed7uDFNJBIgsdhnoe92840928"
hashingAlgorithm="HS256"
expirationTimeMinutes=30

def createJWT(jwtPayload:dict):
    data=jwtPayload.copy()
    expire=datetime.now(timezone.utc)+timedelta(minutes=expirationTimeMinutes)
    data.update({"exp":expire})
    #data/jwt payload contains 'username' and 'exp'
    encoded_jwtoken=jwt.encode(data,algorithm=hashingAlgorithm,key=secretKey)
    return encoded_jwtoken

def verifyToken(token:str,credentials_exception):
    try:
        payload=jwt.decode(token,key=secretKey,algorithms=[hashingAlgorithm])
        userName=payload.get("username")
        if userName is None:
            raise credentials_exception
    #tokenData=ApiSchemas.TokenSchema()
    except JWTError:
        raise credentials_exception
    return userName

def getCurrentUser(token:str =Depends(oauth2_scheme)):
    #print("Inside getCUrrenUser :",token)
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",
                                        headers={"WWW-Authenticate":"Bearer"})
    return verifyToken(token,credentials_exception)