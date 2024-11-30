from fastapi import FastAPI
from .routers import AuthenticationApis, ContactApis,UserApis


app = FastAPI()
app.include_router(AuthenticationApis.router)
app.include_router(ContactApis.router)
app.include_router(UserApis.router)
    




