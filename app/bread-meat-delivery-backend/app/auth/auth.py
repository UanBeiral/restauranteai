from fastapi import Request, HTTPException
from app.config import SUPABASE_PROJECT_URL, SUPABASE_ANON_KEY, INSECURE_SSL
import httpx

def _get_bearer_token(request: Request) -> str:
    auth = request.headers.get("authorization") or request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token ausente")
    return auth.split(" ", 1)[1].strip()

async def verify_supabase_user(request: Request):
    """
    Garante que quem chama a API está logado no Supabase (um único usuário no seu caso).
    Validação feita chamando /auth/v1/user com o token recebido do frontend.
    """
    if not SUPABASE_PROJECT_URL or not SUPABASE_ANON_KEY:
        raise HTTPException(status_code=500, detail="Config do Supabase ausente (.env)")

    token = _get_bearer_token(request)
    url = f"{SUPABASE_PROJECT_URL}/auth/v1/user"
    headers = {"apikey": SUPABASE_ANON_KEY, "Authorization": f"Bearer {token}"}

    try:
        async with httpx.AsyncClient(timeout=10, verify=not INSECURE_SSL) as client:
            resp = await client.get(url, headers=headers)
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Falha ao contatar Supabase Auth: {e!s}")

    if resp.status_code != 200:
        # 401/403 → token inválido/expirado
        raise HTTPException(status_code=401, detail=f"Token inválido ({resp.status_code})")

    return resp.json()
