import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_PROJECT_URL = os.getenv("SUPABASE_PROJECT_URL", "").rstrip("/")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY", "")

SKIP_JWT_VERIFY = os.getenv("SKIP_JWT_VERIFY", "0") == "1"   # DEV only
INSECURE_SSL   = os.getenv("INSECURE_SSL", "0") == "1"       # DEV only

# Logs simples no startup (sem vazar chaves)
if not SUPABASE_PROJECT_URL or not SUPABASE_API_KEY:
    print("[CONFIG] ATENÇÃO: preencha SUPABASE_PROJECT_URL e SUPABASE_API_KEY no .env")
else:
    print("[CONFIG] SUPABASE_PROJECT_URL:", SUPABASE_PROJECT_URL)
    print("[CONFIG] SUPABASE_API_KEY: (definida)")
    if SKIP_JWT_VERIFY:
        print("[CONFIG] SKIP_JWT_VERIFY=1 (DEV)")
    if INSECURE_SSL:
        print("[CONFIG] INSECURE_SSL=1 (DEV, verify=False)")
