from fastapi import FastAPI, HTTPException, APIRouter, status
from pydantic import BaseModel
from db.models.user import User
from db.client import db_cliente
from db.schemas.user import user_schema

router = APIRouter(prefix="/userdb", 
                   tags=["userdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"message":"No encontrado"}})

# Creo entidad

# Lista de usuarios
users_list = []


@router.get("/")
async def users():
    return db_cliente.local.users.find()

# Path
@router.get("/{id}")
async def users(id: int):
    # # Filter devuelve un objeto
    # user = filter(lambda user: user.id == id, users_list)
    # try:
    #     # Esto me permite que no me devuelva una lista
    #     return list(user)[0]
    # except:
    #     return {"error":"No se ha encontrado el usuario"}
    return search_user(id)
    
# Parámetros por query -> URL: userquery/?id=1
@router.get("/")
async def user(id: int, name: str):
    return search_user(id)

# POST
@router.post("/",response_model=User, status_code=201)
async def user(user: User):
    if type(searchuser_by_email(user.email)) == User:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="El usuario ya existe")
    
    # Si lo inserto directamente, el id aparece como null
    user_dict = dict(user)
    
    del user_dict["id"]

    id = db_cliente.local.users.insert_one(user_dict).inserted_id
    
    # El criterio de búsqueda es el id que acabamos de guardar.
    new_user = user_schema(db_cliente.local.users.find_one({"_id": id}))
    
    return User(**new_user)

@router.put("/")
async def user(user: User):

    found = False

    for index, saved_user in enumerate(users_list):
        # Si la id coincide, se actualiza al usuario.
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    
    if not found:
        return {"error":"No se ha actualizado el usuario"}

    return user

# DELETE
@router.delete("/{id}")
async def user(id: int):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
    
    if not found:
        return {"message":"No se ha eliminado el usuario"}
    
def searchuser_by_email(email: str):
    try:
        user = db_cliente.local.users.find_one({"email":email})
        return User(**user_schema(user))
    except:
        return {"error":"No se ha encontrado el usuario"}

def search_user(id: str):
    return ""