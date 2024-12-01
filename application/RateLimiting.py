from time import time

from fastapi import HTTPException,status

class RateLimiter:
    _instance=None
    _userToBuckets={}
    _perUserTokenCount=1
    #No.of requets to serve per each user
    _leakRate=_perUserTokenCount/60   
    @classmethod
    def getInstance(cls):
        if RateLimiter._instance is None:
            RateLimiter._instance=RateLimiter()
        return RateLimiter._instance
    @classmethod
    def acceptRequest(cls,username):
        currTime=time()
        if RateLimiter._userToBuckets.get(username) is None:
            RateLimiter._userToBuckets[username]={"tokenCount":RateLimiter._perUserTokenCount,"lastUsed":currTime}
        elapsed=currTime-RateLimiter._userToBuckets[username]['lastUsed']
        RateLimiter._userToBuckets[username]["tokenCount"]+=(elapsed*RateLimiter._leakRate)
        RateLimiter._userToBuckets[username]["tokenCount"]=min(RateLimiter._userToBuckets[username]["tokenCount"],RateLimiter._perUserTokenCount)
        RateLimiter._userToBuckets[username]["lastUsed"]=currTime

        if RateLimiter._userToBuckets[username]["tokenCount"]>=1:
            RateLimiter._userToBuckets[username]["tokenCount"]-=1
            return
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,detail="Too many requests, try again after sometime!")

