from fastapi import APIRouter, Depends, Request, Query, HTTPException
from app.auth.auth import verify_jwt
from app.config import SUPABASE_PROJECT_URL, SUPABASE_API_KEY
import httpx
from datetime import datetime

router = APIRouter(prefix="/pedidos", tags=["pedidos"])

def format_datetime_br(dt_str):
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        return dt.strftime("%d/%m/%Y %H:%M")
    except Exception:
        return dt_str

def format_money_br(value):
    try:
        return f"R$ {float(value):,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
    except Exception:
        return str(value)

@router.get("/")
async def listar_pedidos(
    request: Request,
    user=Depends(verify_jwt),
    status: str = Query("", description="Filtro de status"),
    data: str = Query("", description="Filtro de data (YYYY-MM-DD)")
):
    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {request.headers.get('authorization').split(' ')[1]}"
    }
    # Monta a query string do Supabase
    query_params = []
    if status:
        query_params.append(f"status=eq.{status}")
    if data:
        query_params.append(f"created_at=gte.{data}T00:00:00Z")
        query_params.append(f"created_at=lte.{data}T23:59:59Z")
    query = "&".join(query_params)
    url = f"{SUPABASE_PROJECT_URL}/rest/v1/pedidos"
    if query:
        url += f"?{query}"
    # Exemplo para trazer também os itens do pedido (ajuste para o nome real da tabela, se necessário)
    url += "&select=*,itens_pedido(*)"

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    pedidos = resp.json()

    # Formatação BR dos campos principais
    for pedido in pedidos:
        if "created_at" in pedido:
            pedido["created_at_br"] = format_datetime_br(pedido["created_at"])
        if "total" in pedido:
            pedido["total_br"] = format_money_br(pedido["total"])
        # Itens (se trouxer via relacionamento)
        if "itens_pedido" in pedido and pedido["itens_pedido"]:
            for item in pedido["itens_pedido"]:
                if "preco" in item:
                    item["preco_br"] = format_money_br(item["preco"])

    return pedidos

@router.patch("/{pedido_id}/status")
async def alterar_status(
    pedido_id: int,
    status: str,
    request: Request,
    user=Depends(verify_jwt)
):
    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {request.headers.get('authorization').split(' ')[1]}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    url = f"{SUPABASE_PROJECT_URL}/rest/v1/pedidos?id=eq.{pedido_id}"
    data = {"status": status}
    async with httpx.AsyncClient() as client:
        resp = await client.patch(url, headers=headers, json=data)
    if resp.status_code not in (200, 204):
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()
