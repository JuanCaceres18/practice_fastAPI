from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel

router = APIRouter()

# Creo entidad
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

# Lista de usuarios
users_list = [User(id= 1,name="Brais",surname="Moure", url="https://www.braismoure.dev", age=19),
            User(id= 2,name="Juan", surname="Cáceres", url="https://www.juancaceres.dev",age=19),
            User(id = 3,name="Pablo", surname="Moure", url="https://www.pablomoure.dev", age=19)
            ]
@router.get("/usersjson")
async def userjson():
    # Devolvemos varios usuarios
    return [{"name":"Brais", "surname":"Moure", "url":"https://www.braismoure.dev", "age":19},
            {"name":"Juan", "surname":"Cáceres", "url":"https://www.juancaceres.dev","age":19},
            {"name":"Pablo", "surname":"Moure", "url":"https://www.pablomoure.dev", "age":19}
            ]

@router.get("/users")
async def users():
    return users_list

# Path
@router.get("/users/{id}")
async def users(id: int):
    # Filter devuelve un objeto
    user = filter(lambda user: user.id == id, users_list)
    try:
        # Esto me permite que no me devuelva una lista
        return list(user)[0]
    except:
        return {"error":"No se ha encontrado el usuario"}
    
# Parámetros por query -> URL: userquery/?id=1
@router.get("/userquery/")
async def user(id: int, name: str):
    return searchuser(id, name)

# POST
@router.post("/user/",response_model=User, status_code=201)
async def user(user: User):
    # Hacer comprobación
    if type(searchuser(user.id, user.name)) == User:
        raise HTTPException(status_code=204, detail="El usuario ya existe")
    
    users_list.append(user)
    return user

@router.put("/user/")
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
@router.delete("/user/{id}")
async def user(id: int):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
    
    if not found:
        return {"message":"No se ha eliminado el usuario"}
def searchuser(id: int, name: str):
    # Filter devuelve un objeto
    user = filter(lambda user: user.id == id and user.name == name, users_list)
    try:
        # Esto me permite que no me devuelva una lista
        return list(user)[0]
    except:
        return {"error":"No se ha encontrado el usuario"}

