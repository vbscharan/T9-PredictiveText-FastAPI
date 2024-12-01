from application.schemas.ApiSchemas import *
from fastapi import status,HTTPException,APIRouter,Depends
from application.models.DatabaseConfiguration import *
from application.controllers.T9PredictiveTextController import *
from application.models.DatabaseConnection import SingletonDatabaseConnection
from application import oauth2
from application.RateLimiting import *

router=APIRouter(tags=['Contact & T9Predictive'])

trie = Trie()

db=SingletonDatabaseConnection.getInstance().db


@router.post("/contacts", status_code=status.HTTP_201_CREATED)
def addContact(payload: ContactCreateSchema,username:str=Depends(oauth2.getCurrentUser)):
    print(username)
    trie.addContact(
        payload.name,
        str(payload.number),
        db.getDatabaseCursor(),
        db.getDatabaseConnection(),username)
    return "'" + payload.name + "' is added to database"


@router.get("/contacts", status_code=status.HTTP_200_OK)
def searchKey(key,username:str=Depends(oauth2.getCurrentUser),page_num: int =1, page_size: int =5):
    RateLimiter().getInstance().acceptRequest(username)
    contacts = trie.searchContact(key, db.getDatabaseCursor(),username)
    if contacts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No contacts were found matching with the given key",
        )
    return contacts
    


@router.put("/contacts/by-name/{oldname}", status_code=status.HTTP_200_OK)
def updateContactName(payload: ContactNameUpdateSchema, oldname: str,username:str=Depends(oauth2.getCurrentUser)):
    RateLimiter().getInstance().acceptRequest(username)
    if oldname==payload.newname:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Old Name and New Name are same",
        )
    res = trie.updateContactName(
        oldname, payload.newname, db.getDatabaseCursor(), db.getDatabaseConnection()
    )
    if res == "oldname was not found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="'" + oldname + "' was not found in the database",
        )
    return "'" + oldname + "'is updated to '" + payload.newname + "'"
    #return {"New Name":payload.newname,"Message":"The contact name is updated"}


@router.put("/contacts/by-number/{oldnumber}", status_code=status.HTTP_200_OK)
def updateContactNumber(payload: ContactNumberUpdateSchema, oldnumber: int,username:str=Depends(oauth2.getCurrentUser)):
    RateLimiter().getInstance().acceptRequest(username)
    if oldnumber==payload.newnumber:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Old Number and New Number are same",
        )
    res = trie.updateContactNumber(
        str(oldnumber),
        str(payload.newnumber),
        db.getDatabaseCursor(),
        db.getDatabaseConnection(),username
    )
    if res == "oldnumber was not found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="'" + str(oldnumber) + "' was not found in the database",
        )
    #return {"New Number":payload.newnumber,"Message":"The mobile number is updated"}
    return "'" + str(oldnumber) + "'is updated to '" + str(payload.newnumber) + "'"


@router.delete("/contacts/{name}", status_code=status.HTTP_204_NO_CONTENT)
def deleteContactName(name,username:str=Depends(oauth2.getCurrentUser)):
    if not trie.deleteContactName(
        name, db.getDatabaseCursor(), db.getDatabaseConnection(),username
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="'" + name + "' was not found in database",
        )