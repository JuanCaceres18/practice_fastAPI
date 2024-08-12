from fastapi import FastAPI, HTTPException, APIRouter, status
from pydantic import BaseModel
from db.models.user import User
from db.client import db_cliente
from db.schemas.user import user_schema, users_schema
from bson import ObjectId
from typing import List

router = APIRouter(prefix="/userdb", 
                   tags=["userdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"message":"No encontrado"}})

# Creo entidad

# Lista de usuarios
users_list = []


@router.get("/", response_model=List[User])
async def users():
    return users_schema(db_cliente.local.users.find())

# Path
@router.get("/{id}")
async def users(id: int):
    found = db_cliente.local.users

    return search_user("_id", ObjectId(id))
    
# Parámetros por query -> URL: userquery/?id=1
@router.get("/")
async def user(id: int, name: str):
    return search_user("_id", ObjectId(id))

# POST
@router.post("/",response_model=User, status_code=201)
async def user(user: User):
    if type(search_user("email", id)) == User:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="El usuario ya existe")
    
    # Si lo inserto directamente, el id aparece como null
    user_dict = dict(user)
    
    del user_dict["id"]

    id = db_cliente.local.users.insert_one(user_dict).inserted_id
    
    # El criterio de búsqueda es el id que acabamos de guardar.
    new_user = user_schema(db_cliente.local.users.find_one({"_id": id}))
    
    return User(**new_user)

@router.put("/", response_model=User)
async def user(user: User):
    
    user_dict = dict(user)
    del user_dict["id"]

    try:
        db_cliente.local.users.find_one_and_replace({"_id":ObjectId(user.id)}, user_dict)
    except:
        return {"error":"No se ha actualizado el usuario"}

    return search_user({"_id":ObjectId(id)})

# DELETE
@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def user(id: str):

    found = db_cliente.local.users.find_one_and_delete({"_id":ObjectId(id)})
    
    if not found:
        return {"message":"No se ha eliminado el usuario"}
    
def search_user(field: str, key: str):
    try:
        user = db_cliente.local.users.find_one({"email":email})
        return User(**user_schema(user))
    except:
        return {"error":"No se ha encontrado el usuario"}

def search_user(id: str):
    return ""