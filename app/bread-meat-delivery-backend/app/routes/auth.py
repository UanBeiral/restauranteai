# app/bread-meat-delivery-backend/app/routes/auth.py
# Autenticação por código único (ACCESS_CODE) + cookie bm_token
import os, jwt
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, HTTPException, status, Response, Cookie, Depends
from pydantic import BaseModel

# Garante que o .env seja lido (load_dotenv em app/config.py)
from app import config as _cfg  # noqa: F401

router = APIRouter(prefix="/auth", tags=["auth"])

ACCESS_CODE = (os.getenv("ACCESS_CODE") or "").strip()
JWT_SECRET = os.getenv("JWT_SECRET") or "change-me"
ALGO = "HS256"
COOKIE_SECURE = (os.getenv("COOKIE_SECURE") or "false").lower() == "true"
TOKEN_TTL_HOURS = int(os.getenv("TOKEN_TTL_HOURS") or "12")

class CodeIn(BaseModel):
  code: str

def _sign(sub: str) -> str:
  now = datetime.now(tz=timezone.utc)
  payload = {
      "sub": sub,
      "iat": int(now.timestamp()),
      "exp": int((now + timedelta(hours=TOKEN_TTL_HOURS)).timestamp()),
  }
  return jwt.encode(payload, JWT_SECRET, algorithm=ALGO)

def _verify(token: str):
  try:
    return jwt.decode(token, JWT_SECRET, algorithms=[ALGO])
  except jwt.PyJWTError:
    return None

@router.post("/verify")
def verify(body: CodeIn, response: Response):
  if not ACCESS_CODE:
    raise HTTPException(status_code=500, detail="access_code_not_configured")
  code = (body.code or "").strip()
  if code != ACCESS_CODE:
    raise HTTPException(status_code=401, detail="invalid_code")

  token = _sign("passcode")
  # Cookie first-party (localhost): SameSite=Lax funciona
  response.set_cookie(
      "bm_token",
      token,
      path="/",
      httponly=False,     # se quiser ocultar do JS, troque para True
      secure=COOKIE_SECURE,
      samesite="lax",
      max_age=TOKEN_TTL_HOURS * 3600,
  )
  return {"ok": True}

def get_user(bm_token: str | None = Cookie(default=None, alias="bm_token")):
  if not bm_token:
    raise HTTPException(status_code=401, detail="missing_token")
  data = _verify(bm_token)
  if not data:
    raise HTTPException(status_code=401, detail="invalid_token")
  return {"sub": data.get("sub")}

@router.get("/ping")
def ping(user=Depends(get_user)):
  return {"ok": True, "sub": user["sub"]}

@router.post("/logout", status_code=204)
def logout(response: Response):
  response.delete_cookie("bm_token", path="/")
  return
