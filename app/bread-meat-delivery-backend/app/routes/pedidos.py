# app/routes/pedidos.py
from fastapi import APIRouter, Depends, Query, HTTPException, Body
from pydantic import BaseModel
from app.auth.auth import verify_supabase_user
from app.config import SUPABASE_PROJECT_URL, SUPABASE_SERVICE_ROLE_KEY, INSECURE_SSL
from datetime import datetime
import httpx

router = APIRouter(
    prefix="/pedidos",
    tags=["pedidos"],
    dependencies=[Depends(verify_supabase_user)],  # exige login Supabase (sbtoken)
)

# -----------------------
# Helpers de formatação BR
# -----------------------
def format_money_br(value) -> str:
    try:
        return f"R$ {float(value):,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
    except Exception:
        return "" if value is None else str(value)

def format_datetime_br(dt_str: str) -> str:
    if not dt_str:
        return ""
    try:
        # aceita "2025-07-15T00:00:00Z" ou timestamptz ISO
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        return dt.strftime("%d/%m/%Y %H:%M")
    except Exception:
        return dt_str

def format_distance_km_br(val) -> str:
    try:
        return f"{float(val):,.2f} km".replace(",", "v").replace(".", ",").replace("v", ".")
    except Exception:
        return "" if val is None else str(val)

def format_eta_br(eta_str: str) -> str:
    # interval do Postgres costuma vir como "HH:MM:SS" ou "1 day 02:30:00"
    if not eta_str:
        return ""
    try:
        if "day" in eta_str:
            parts = eta_str.split("day")
            days = int(parts[0].strip())
            hhmmss = parts[1].strip()
        else:
            days = 0
            hhmmss = eta_str.strip()
        hh, mm, ss = [int(x) for x in hhmmss.split(":")]
        total_min = days * 24 * 60 + hh * 60 + mm + (1 if ss >= 30 else 0)
        if total_min < 60:
            return f"{total_min} min"
        h, m = divmod(total_min, 60)
        return f"{h}h {m}m" if m else f"{h}h"
    except Exception:
        return eta_str

# -----------------------
# HTTP helpers
# -----------------------
def _sr_headers() -> dict:
    if not SUPABASE_PROJECT_URL or not SUPABASE_SERVICE_ROLE_KEY:
        raise HTTPException(status_code=500, detail="Faltam SUPABASE_PROJECT_URL/SERVICE_ROLE_KEY no .env")
    # Service Role ignora RLS (servidor somente)
    return {
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": "application/json",
    }

# -----------------------
# Endpoints
# -----------------------
@router.get("")
@router.get("/")
async def listar_pedidos(
    status: str = Query("", description="Filtro de status"),
    data:   str = Query("", description="Filtro de data (YYYY-MM-DD)"),
):
    headers = _sr_headers()
    params  = [("select", "*"), ("order", "id.asc")]

    if status:
        params.append(("status", f"eq.{status}"))

    # aceita data em YYYY-MM-DD (ex.: 2025-07-15). Se vier vazia, não filtra.
    if data:
        # faixa do dia inteiro (UTC)
        params.append(("created_at", f"gte.{data}T00:00:00Z"))
        params.append(("created_at", f"lte.{data}T23:59:59Z"))

    url = f"{SUPABASE_PROJECT_URL}/rest/v1/pedidos"
    try:
        async with httpx.AsyncClient(timeout=15, verify=not INSECURE_SSL) as client:
            resp = await client.get(url, headers=headers, params=params)
    except httpx.ConnectError as e:
        raise HTTPException(502, f"Conexão ao Supabase falhou: {e!s}")
    except httpx.HTTPError as e:
        raise HTTPException(502, f"HTTP erro ao chamar Supabase: {e!s}")
    except Exception as e:
        raise HTTPException(500, f"Erro interno listar_pedidos: {type(e).__name__}: {e!s}")

    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)

    try:
        pedidos = resp.json()
    except ValueError:
        raise HTTPException(502, f"Resposta inesperada do Supabase: {resp.text[:200]}")

    for p in pedidos:
        p["created_at_br"]  = format_datetime_br(p.get("created_at"))
        p["updated_at_br"]  = format_datetime_br(p.get("updated_at"))
        p["total_br"]       = format_money_br(p.get("total"))
        p["frete_br"]       = format_money_br(p.get("frete"))
        p["distance_km_br"] = format_distance_km_br(p.get("distance_km"))
        p["eta_br"]         = format_eta_br(p.get("eta"))

    return pedidos

@router.get("/{pedido_id}")
async def obter_pedido_por_id(pedido_id: int):
    headers = _sr_headers()
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
        raise HTTPException(502, f"HTTP erro ao chamar Supabase: {e!s}")
    except Exception as e:
        raise HTTPException(500, f"Erro interno obter_pedido_por_id: {type(e).__name__}: {e!s}")

    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)

    rows = resp.json()
    if not rows:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    p = rows[0]
    p["created_at_br"]  = format_datetime_br(p.get("created_at"))
    p["updated_at_br"]  = format_datetime_br(p.get("updated_at"))
    p["total_br"]       = format_money_br(p.get("total"))
    p["frete_br"]       = format_money_br(p.get("frete"))
    p["distance_km_br"] = format_distance_km_br(p.get("distance_km"))
    p["eta_br"]         = format_eta_br(p.get("eta"))

    if "order_items" in p and isinstance(p["order_items"], list):
        for it in p["order_items"]:
            it["price_br"]      = format_money_br(it.get("price"))
            it["item_total_br"] = format_money_br(it.get("item_total"))

    return p

class StatusPayload(BaseModel):
    status: str

@router.patch("/{pedido_id}/status")
async def alterar_status(pedido_id: int, payload: StatusPayload = Body(...)):
    headers = _sr_headers()
    url = f"{SUPABASE_PROJECT_URL}/rest/v1/pedidos"
    params = [("id", f"eq.{pedido_id}")]
    try:
        async with httpx.AsyncClient(timeout=15, verify=not INSECURE_SSL) as client:
            resp = await client.patch(url, headers=headers, params=params, json={"status": payload.status})
    except httpx.HTTPError as e:
        raise HTTPException(502, f"HTTP erro ao chamar Supabase: {e!s}")
    except Exception as e:
        raise HTTPException(500, f"Erro interno alterar_status: {type(e).__name__}: {e!s}")

    if resp.status_code not in (200, 204):
        raise HTTPException(status_code=resp.status_code, detail=resp.text)

    return resp.json()
