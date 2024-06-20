from supabase import create_client
import os

supabase_client = create_client(
    supabase_url=os.environ.get("SUPABASE_URL"),
    supabase_key=os.environ.get("SUPABASE_ANON_KEY")
)