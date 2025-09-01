from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import pedidos

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrinja em produção (ex.: ["http://localhost:3000"])
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Authorization", "Content-Type", "*"],
)

app.include_router(pedidos.router)

@app.get("/")
async def root():
    return {"msg": "API Bread&Meat Delivery (Auth Supabase + SR DB)"}
