

from supabase import create_client
from config import Config

supabase = create_client(
    Config.SUPABASE_URL,
    Config.SUPABASE_KEY
)

BUCKET = Config.SUPABASE_BUCKET


import httpx
import httpcore

print("HTTPX VERSION:", httpx.__version__)
print("HTTPCORE VERSION:", httpcore.__version__)