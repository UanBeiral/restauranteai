# app/routes/auth.py  (arquivo novo, tudo em um lugar)
import os, jwt
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, HTTPException, status, Response, Cookie, Depends
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])

ACCESS_CODE = os.getenv("ACCESS_CODE") or ""
JWT_SECRET = os.getenv("JWT_SECRET") or "change-me"
ALGO = "HS256"
COOKIE_SECURE = (os.getenv("COOKIE_SECURE") or "false").lower() == "true"
TOKEN_TTL_HOURS = int(os.getenv("TOKEN_TTL_HOURS") or "12")

class CodeIn(BaseModel):
    code: str

def _make_token():
    now = datetime.now(timezone.utc)
    payload = {
        "sub": "passcode",
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(hours=TOKEN_TTL_HOURS)).timestamp()),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGO)

def _verify(token: str):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[ALGO])
    except jwt.PyJWTError:
        return None

@router.post("/verify", status_code=204)
def verify_code(body: CodeIn, response: Response):
    if body.code.strip() != ACCESS_CODE.strip():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid_code")
    token = _make_token()
    response.set_cookie(
        key="bm_token",
        value=token,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="lax",
        max_age=TOKEN_TTL_HOURS * 3600,
        path="/",
    )
    return

def get_user(bm_token: str | None = Cookie(default=None)):
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
