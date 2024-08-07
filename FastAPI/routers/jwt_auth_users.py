from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 2
SECRET = "2275411189690520dc48e9eeab05a90f1b0a790dff3c47470f8473a2a9615803"

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# Algoritmo de encriptación
crypt = CryptContext(schemes=["bcrypt"])

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
        "password": "$2a$12$QFNthjnt7iK7.ZeTVh6UC.PiyOFXPuUqoHYqwoMjpWHmj0gX.IH6q"
    },
    "mouredev2":{
        "username": "mouredev2",
        "full_name": "Brais Moure 2",
        "email": "braismoure2@mouredev.com",
        "disabled": True,
        "password": "$2a$12$YGC491csi.xwUM.mxbmbYOWFKVXVvvyYYqYLwDAb1e4UWI/vi3fpq"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales de autenticación inválidas",
            headers={"WWW-Authenticate":"Bearer"}
        )
    
    try:
        # Obtengo el username del JSON
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
    except JWTError:
        raise exception
    
    return search_user(username)

async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    # Voy a mi base de datos y busco mi usuario.
    user_db = users_db.get(form.username)
    # Si no encuentro el usuario, lanzo la excepción
    if not user_db:
        raise HTTPException(
            status_code=400, details="El usuario no es correcto"
        )
    
    user = search_user_db(form.username)
    # Comprobamos si la contraseña es la correcta
    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=400, detail="La contraseña no es correcta"
        )

    
    access_token = {"sub": user.username,
                    "exp":datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION) }
    
    # El token de autenticación es el nombre del usuario
    return {"access_token":jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type":"bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user