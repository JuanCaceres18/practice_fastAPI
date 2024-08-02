from fastapi import APIRouter

products_list = ["Producto 1", "Producto 2", "producto 3", "Producto 4"]

router = APIRouter(prefix="/products", 
                   tags=["products"],
                   responses={404: {"message":"No encontrado"}})

@router.get("/")
async def products():
    return products_list


@router.get("/{id}")
async def products(id: int):
    return products_list[id]