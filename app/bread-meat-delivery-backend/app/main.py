from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import pedidos
from app.routes import debug  # <---
from app.routes.auth import router as auth_router 

app = FastAPI()
origins = ["http://localhost:3000", "https://seu-dominio-frontend.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins   ,  # restrinja em prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Authorization", "Content-Type", "*"],
)

app.include_router(pedidos.router)
app.include_router(debug.router)  # <---
app.include_router(auth_router)

@app.get("/")
async def root():
    return {"msg": "API Bread&Meat Delivery"}

@app.get("/health")
def health(): return {"ok": True}