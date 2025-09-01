import os
from dotenv import load_dotenv
load_dotenv()

# Supabase
SUPABASE_PROJECT_URL      = os.getenv("SUPABASE_PROJECT_URL", "").rstrip("/")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")  # SR (server only)
SUPABASE_ANON_KEY         = os.getenv("SUPABASE_ANON_KEY", "")          # para validar /auth/v1/user

# DEV: ignorar verificação SSL (ambientes com proxy/cert corporativo)
INSECURE_SSL = os.getenv("INSECURE_SSL", "0") == "1"

print("[CONFIG] SUPABASE_PROJECT_URL:", "ok" if SUPABASE_PROJECT_URL else "vazio")
print("[CONFIG] SERVICE_ROLE_KEY   :", "ok" if SUPABASE_SERVICE_ROLE_KEY else "vazio")
print("[CONFIG] ANON_KEY           :", "ok" if SUPABASE_ANON_KEY else "vazio")
if INSECURE_SSL:
    print("[CONFIG] INSECURE_SSL=1 (verify=False)")
