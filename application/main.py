from fastapi import FastAPI,Request
from .routers import AuthenticationApis, ContactApis,UserApis
from .RateLimiting import RateLimiter


app = FastAPI()
@app.middleware("http")
def checkRateLimiting(req:Request,call_next):
    RateLimiter().getInstance().acceptRequest(req.client.host)
    res=call_next(req)
    return res

app.include_router(AuthenticationApis.router)
app.include_router(ContactApis.router)
app.include_router(UserApis.router)
    




