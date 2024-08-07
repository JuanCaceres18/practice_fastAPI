from fastapi import FastAPI
from routers.products import products
from routers import users, products, jwt_auth_users, basic_auth_users
from fastapi.staticfiles import StaticFiles

# Contexto
app = FastAPI()

app.include_router(products.router)
app.include_router(users.router)
app.include_router(jwt_auth_users.router)
app.include_router(basic_auth_users.router)
# Incluir archivos estáticos
app.mount("/statico", StaticFiles(directory="static"), name="statico")

# Operación GET
@app.get("/")
async def root():
    return "Hola mundo"

@app.get("/url")
async def root():
    return {"url_curso":"https://youtube.com"}

# Iniciar server uvicorn main:app --reload

# Swagger:http://127.0.0.1:8000/docs
# Redocly: http://127.0.0.1:8000/redoc