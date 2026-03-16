from fastapi import FastAPI
from src.api.api_v1.endpoints import auth
# Импортируем остальные модули, но обрабатываем возможное отсутствие router
try:
    from src.api.api_v1.endpoints import users
    users_router = users.router
except (ImportError, AttributeError):
    from fastapi import APIRouter
    users_router = APIRouter()
    @users_router.get("/")
    async def temp_users():
        return {"message": "Users endpoint (temporary)"}

try:
    from src.api.api_v1.endpoints import categories
    categories_router = categories.router
except (ImportError, AttributeError):
    from fastapi import APIRouter
    categories_router = APIRouter()
    @categories_router.get("/")
    async def temp_categories():
        return {"message": "Categories endpoint (temporary)"}

try:
    from src.api.api_v1.endpoints import products
    products_router = products.router
except (ImportError, AttributeError):
    from fastapi import APIRouter
    products_router = APIRouter()
    @products_router.get("/")
    async def temp_products():
        return {"message": "Products endpoint (temporary)"}

app = FastAPI(title="FastAPI Shop")

# Подключаем роутеры
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
app.include_router(categories_router, prefix="/api/v1/categories", tags=["categories"])
app.include_router(products_router, prefix="/api/v1/products", tags=["products"])

@app.get("/")
async def root():
    return {"message": "Hello World"}