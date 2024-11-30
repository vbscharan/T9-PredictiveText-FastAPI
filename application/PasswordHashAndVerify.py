from passlib.context import CryptContext

hashing=CryptContext(schemes='bcrypt',deprecated='auto')

def hash(password:str):
    return hashing.hash(password)

def verify(plain,hashed):
    return hashing.verify(plain,hashed)