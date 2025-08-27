from fastapi import Request, HTTPException
from app.config import SUPABASE_PROJECT_URL, SUPABASE_API_KEY, SKIP_JWT_VERIFY, INSECURE_SSL
import httpx

def _get_bearer_token(request: Request) -> str:
    auth = request.headers.get("authorization") or request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token ausente")
    return auth.split(" ", 1)[1].strip()

async def verify_jwt(request: Request):
    token = _get_bearer_token(request)

    if SKIP_JWT_VERIFY:
        return {"sub": "dev-skip", "role": "authenticated"}

    if not SUPABASE_PROJECT_URL or not SUPABASE_API_KEY:
        raise HTTPException(status_code=500, detail="Falta SUPABASE_PROJECT_URL/API_KEY no .env")

    url = f"{SUPABASE_PROJECT_URL}/auth/v1/user"
    headers = {"apikey": SUPABASE_API_KEY, "Authorization": f"Bearer {token}"}

    try:
        async with httpx.AsyncClient(timeout=10, verify=not INSECURE_SSL) as client:
            resp = await client.get(url, headers=headers)
    except httpx.HTTPError as e:
        # Erro de rede/SSL/timeouts
        raise HTTPException(status_code=502, detail=f"Falha ao contatar Supabase Auth: {e!s}")

    if resp.status_code != 200:
        # 401/403: token inválido/expirado; 404 raríssimo
        raise HTTPException(status_code=401, detail=f"Token inválido no Supabase ({resp.status_code})")

    return resp.json()
