# app/routes/pedidos.py
from fastapi import APIRouter, Depends, Request, Query, HTTPException, Body
from pydantic import BaseModel
from app.auth.auth import verify_jwt
from app.config import SUPABASE_PROJECT_URL, SUPABASE_API_KEY, INSECURE_SSL
from datetime import datetime
import httpx

router = APIRouter(
    prefix="/pedidos",
    tags=["pedidos"],
    dependencies=[Depends(verify_jwt)],
)

def format_datetime_br(dt_str: str) -> str:
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        return dt.strftime("%d/%m/%Y %H:%M")
    except Exception:
        return dt_str

def format_money_br(value) -> str:
    try:
        return f"R$ {float(value):,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
    except Exception:
        return str(value)

def _get_bearer_token(request: Request) -> str:
    auth = request.headers.get("authorization") or request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token ausente")
    return auth.split(" ", 1)[1].strip()

@router.get("")
@router.get("/")
async def listar_pedidos(
    request: Request,
    status: str = Query("", description="Filtro de status"),
    data:   str = Query("", description="Filtro de data (YYYY-MM-DD)"),
):
    token = _get_bearer_token(request)
    if not SUPABASE_PROJECT_URL or not SUPABASE_API_KEY:
        raise HTTPException(status_code=500, detail="Falta SUPABASE_PROJECT_URL/API_KEY no .env")

    headers = {"apikey": SUPABASE_API_KEY, "Authorization": f"Bearer {token}"}
    params  = [("select", "*")]
    if status:
        params.append(("status", f"eq.{status}"))
    if data:
        params.append(("created_at", f"gte.{data}T00:00:00Z"))
        params.append(("created_at", f"lte.{data}T23:59:59Z"))

    url = f"{SUPABASE_PROJECT_URL}/rest/v1/pedidos"
    try:
        async with httpx.AsyncClient(timeout=15, verify=not INSECURE_SSL) as client:
            resp = await client.get(url, headers=headers, params=params)
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Falha ao contatar Supabase REST: {e!s}")

    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)

    pedidos = resp.json()
    for p in pedidos:
        if p.get("created_at"):
            p["created_at_br"] = format_datetime_br(p["created_at"])
        if "total" in p:
            p["total_br"] = format_money_br(p["total"])
        # relação não vem aqui na listagem (intencional, para ficar leve)

    return pedidos

@router.get("/{pedido_id}")
async def obter_pedido_por_id(pedido_id: int, request: Request):
    token = _get_bearer_token(request)
    if not SUPABASE_PROJECT_URL or not SUPABASE_API_KEY:
        raise HTTPException(status_code=500, detail="Falta SUPABASE_PROJECT_URL/API_KEY no .env")

    headers = {"apikey": SUPABASE_API_KEY, "Authorization": f"Bearer {token}"}
    params = [
        ("id", f"eq.{pedido_id}"),
        ("select", "*,order_items(*)"),
        ("limit", "1")
    ]
    url = f"{SUPABASE_PROJECT_URL}/rest/v1/pedidos"
    try:
        async with httpx.AsyncClient(timeout=15, verify=not INSECURE_SSL) as client:
            resp = await client.get(url, headers=headers, params=params)
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Falha ao contatar Supabase REST: {e!s}")

    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)

    rows = resp.json()
    if not rows:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    p = rows[0]
    if p.get("created_at"):
        p["created_at_br"] = format_datetime_br(p["created_at"])
    if "total" in p:
        p["total_br"] = format_money_br(p["total"])
    if "order_items" in p and isinstance(p["order_items"], list):
        for item in p["order_items"]:
            val = item.get("price", item.get("preco"))
            if val is not None:
                br = format_money_br(val)
                item.setdefault("price_br", br)
                item.setdefault("preco_br", br)

    return p

class StatusPayload(BaseModel):
    status: str

@router.patch("/{pedido_id}/status")
async def alterar_status(
    pedido_id: int,
    payload: StatusPayload = Body(...),
    request: Request = None,
):
    token = _get_bearer_token(request)
    if not SUPABASE_PROJECT_URL or not SUPABASE_API_KEY:
        raise HTTPException(status_code=500, detail="Falta SUPABASE_PROJECT_URL/API_KEY no .env")

    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }
    url = f"{SUPABASE_PROJECT_URL}/rest/v1/pedidos"
    params = [("id", f"eq.{pedido_id}")]

    try:
        async with httpx.AsyncClient(timeout=15, verify=not INSECURE_SSL) as client:
            resp = await client.patch(url, headers=headers, params=params, json={"status": payload.status})
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Falha ao contatar Supabase REST: {e!s}")

    if resp.status_code not in (200, 204):
        raise HTTPException(status_code=resp.status_code, detail=resp.text)

    return resp.json()
