from fastapi import APIRouter, Depends, Request, Query
from app.auth.auth import verify_jwt

# Exemplo estático; substitua por integração com Supabase depois!
EXEMPLO_PEDIDOS = [
    {"id": 1, "cliente": "João", "status": "solicitado", "endereco": "Rua Teste, 10", "total": 80, "itens":[{"nome":"Costela","qtd":1,"preco":80}]},
    {"id": 2, "cliente": "Maria", "status": "em_preparo", "endereco": "Av. Exemplo, 123", "total": 50, "itens":[{"nome":"Picanha","qtd":1,"preco":50}]},
]

router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@router.get("/")
async def listar_pedidos(
    request: Request,
    status: str = Query(default=None, description="Status do pedido"),
    data: str = Query(default=None, description="Data (aaaa-mm-dd)"),
    user=Depends(verify_jwt)
):
    pedidos = EXEMPLO_PEDIDOS
    if status:
        pedidos = [p for p in pedidos if p["status"] == status]
    return pedidos

@router.get("/{pedido_id}")
async def detalhe_pedido(pedido_id: int, request: Request, user=Depends(verify_jwt)):
    pedido = next((p for p in EXEMPLO_PEDIDOS if p["id"] == pedido_id), None)
    if not pedido:
        return {"erro": "Pedido não encontrado"}
    return pedido

@router.patch("/{pedido_id}/status")
async def alterar_status(pedido_id: int, status: str, request: Request, user=Depends(verify_jwt)):
    # Aqui você faria o update real na tabela do Supabase!
    return {"msg": f"Pedido {pedido_id} alterado para {status}"}