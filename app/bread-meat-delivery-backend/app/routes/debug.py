# app/routes/debug.py
from fastapi import APIRouter, Request, HTTPException
from app.config import (
    SUPABASE_PROJECT_URL, SUPABASE_SERVICE_ROLE_KEY, SUPABASE_ANON_KEY, INSECURE_SSL
)
import httpx

router = APIRouter(prefix="/__debug", tags=["__debug"])

@router.get("/health")
def health():
    return {
        "project_url": bool(SUPABASE_PROJECT_URL),
        "sr_key": bool(SUPABASE_SERVICE_ROLE_KEY),
        "anon_key": bool(SUPABASE_ANON_KEY),
        "insecure_ssl": INSECURE_SSL,
    }

@router.get("/ping-auth")
async def ping_auth(request: Request):
    """Valida o token do Supabase enviado no Authorization: Bearer <sbtoken>"""
    token = (request.headers.get("authorization") or "").split("Bearer ")[-1].strip()
    if not token:
        raise HTTPException(400, "Envie Authorization: Bearer <sbtoken>")
    if not SUPABASE_PROJECT_URL or not SUPABASE_ANON_KEY:
        raise HTTPException(500, "Faltam SUPABASE_PROJECT_URL/ANON_KEY no .env")

    url = f"{SUPABASE_PROJECT_URL}/auth/v1/user"
    headers = {"apikey": SUPABASE_ANON_KEY, "Authorization": f"Bearer {token}"}
    try:
        async with httpx.AsyncClient(timeout=10, verify=not INSECURE_SSL) as c:
            r = await c.get(url, headers=headers)
        ct = r.headers.get("content-type", "")
        body = r.json() if ct.startswith("application/json") else r.text
        return {"status": r.status_code, "body": body}
    except httpx.HTTPError as e:
        raise HTTPException(502, f"Falha ao contatar Supabase Auth: {e!s}")

@router.get("/ping-rest-sr")
async def ping_rest_sr():
    """Chama o PostgREST com Service Role (bypass RLS) só pra validar SR/SSL/rede"""
    if not SUPABASE_PROJECT_URL or not SUPABASE_SERVICE_ROLE_KEY:
        raise HTTPException(500, "Faltam SUPABASE_PROJECT_URL/SERVICE_ROLE_KEY no .env")

    url = f"{SUPABASE_PROJECT_URL}/rest/v1/pedidos?select=id&limit=1"
    headers = {
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
    }
    try:
        async with httpx.AsyncClient(timeout=10, verify=not INSECURE_SSL) as c:
            r = await c.get(url, headers=headers)
        ct = r.headers.get("content-type", "")
        body = r.json() if ct.startswith("application/json") else r.text
        return {"status": r.status_code, "body": body}
    except httpx.HTTPError as e:
        raise HTTPException(502, f"Falha ao contatar Supabase REST: {e!s}")
