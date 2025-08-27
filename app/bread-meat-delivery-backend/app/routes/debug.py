from fastapi import APIRouter, Request, Depends, HTTPException
from app.auth.auth import verify_jwt, _get_bearer_token
from app.config import SUPABASE_PROJECT_URL, SUPABASE_API_KEY, INSECURE_SSL
import httpx

router = APIRouter(prefix="/__debug", tags=["__debug"])

@router.get("/headers")
async def headers(request: Request):
    return dict(request.headers)

@router.get("/whoami")
async def whoami(user=Depends(verify_jwt)):
    return user

@router.get("/ping-auth")
async def ping_auth(request: Request):
    """Testa /auth/v1/user com o token da requisição (sem Depends)."""
    if not SUPABASE_PROJECT_URL or not SUPABASE_API_KEY:
        raise HTTPException(status_code=500, detail="Falta SUPABASE_PROJECT_URL/API_KEY no .env")
    token = _get_bearer_token(request)
    url = f"{SUPABASE_PROJECT_URL}/auth/v1/user"
    headers = {"apikey": SUPABASE_API_KEY, "Authorization": f"Bearer {token}"}
    try:
        async with httpx.AsyncClient(timeout=10, verify=not INSECURE_SSL) as client:
            r = await client.get(url, headers=headers)
        return {"status": r.status_code, "body": r.json() if r.headers.get("content-type","").startswith("application/json") else r.text}
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Falha ao contatar Supabase Auth: {e!s}")

@router.get("/ping-rest")
async def ping_rest(request: Request):
    """Testa /rest/v1/pedidos com token da requisição (sem filtros)."""
    if not SUPABASE_PROJECT_URL or not SUPABASE_API_KEY:
        raise HTTPException(status_code=500, detail="Falta SUPABASE_PROJECT_URL/API_KEY no .env")
    token = _get_bearer_token(request)
    url = f"{SUPABASE_PROJECT_URL}/rest/v1/pedidos?select=*"
    headers = {"apikey": SUPABASE_API_KEY, "Authorization": f"Bearer {token}"}
    try:
        async with httpx.AsyncClient(timeout=10, verify=not INSECURE_SSL) as client:
            r = await client.get(url, headers=headers)
        return {"status": r.status_code, "body": r.json() if r.headers.get("content-type","").startswith("application/json") else r.text}
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Falha ao contatar Supabase REST: {e!s}")
