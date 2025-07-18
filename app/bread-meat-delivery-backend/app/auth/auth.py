from fastapi import Request, HTTPException, status, Depends
from jose import jwt
from app.config import SUPABASE_JWT_SECRET

def verify_jwt(request: Request):
    auth = request.headers.get("authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token ausente")
    token = auth.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=["RS256"])
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")
