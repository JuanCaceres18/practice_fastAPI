from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "mouredev":{
        "username": "mouredev",
        "full_name": "Brais Moure",
        "email": "braismoure@mouredev.com",
        "disabled": False,
        "password": "123456"
    },
    "mouredev2":{
        "username": "mouredev2",
        "full_name": "Brais Moure 2",
        "email": "braismoure2@mouredev.com",
        "disabled": True,
        "password": "654321"
    }

}

def search_user(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales de autenticación inválidas",
            headers={"WWW-Authenticate":"Bearer"}
        )

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    # Voy a mi base de datos y busco mi usuario.
    user_db = users_db.get(form.username)
    # Si no encuentro el usuario, lanzo la excepción
    if not user_db:
        raise HTTPException(
            status_code=400, details="El usuario no es correcto"
        )
    
    user = search_user(form.username)
    # Comprobamos si la contraseña es la correcta
    if not form.password == user.password:
        raise HTTPException(
            status_code=400, detail="La contraseña no es correcta"
        )
    # El token de autenticación es el nombre del usuario
    return {"access_token":user.username, "token_type":"bearer"}

@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user