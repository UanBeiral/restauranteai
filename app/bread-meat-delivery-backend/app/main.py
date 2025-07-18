from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import pedidos

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Altere para o domínio do seu frontend em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pedidos.router)

@app.get("/")
async def root():
    return {"msg": "API Bread&Meat Delivery"}
