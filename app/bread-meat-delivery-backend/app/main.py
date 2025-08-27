from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import pedidos
from app.routes import debug

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrinja em prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Authorization", "Content-Type", "*"],
)

app.include_router(pedidos.router)
app.include_router(debug.router)

@app.get("/")
async def root():
    return {"msg": "API Bread&Meat Delivery"}
