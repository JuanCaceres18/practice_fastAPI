from fastapi import FastAPI
from routers.products import products
from routers import users, products
from fastapi.staticfiles import StaticFiles

# Contexto
app = FastAPI()

app.include_router(products.router)
app.include_router(users.router)
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