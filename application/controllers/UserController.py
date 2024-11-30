from ..schemas.ApiSchemas import *

class User:

    def __init__(self):
        pass

    def createUser(self,conn,cursor,payload:UserCreateSchema):
        cursor.execute("SELECT username from users where username=(%s)",(payload.username,))
        k=cursor.fetchone()

        if k and k.get('username') is not None:
            return "Username already exists"
        if payload.email is None:
            cursor.execute("INSERT into users (username,password) values(%s,%s)",(payload.username,payload.password))
        else:
            cursor.execute("INSERT into users (username,email,password) values(%s,%s,%s)",(payload.username,payload.email,payload.password))
        conn.commit()
        return "User is created"