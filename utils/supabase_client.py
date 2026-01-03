import os
from supabase import create_client, Client
from flask import current_app

_supabase_client = None

def get_supabase_client() -> Client:
    """
    Get or create a singleton Supabase client.
    """
    global _supabase_client
    
    if _supabase_client is None:
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        
        if not url or not key:
            # Fallback for when current_app isn't available or env vars missing in context
            # (Though in this app they should be loaded by dotenv)
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment")
            
        _supabase_client = create_client(url, key)
        
    return _supabase_client
