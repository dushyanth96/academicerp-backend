import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

if not url or not key:
    print("❌ URL or KEY missing in .env")
    print(f"URL: {url}")
    print(f"KEY: {key}")
    exit(1)

print(f"Connecting to: {url}")

try:
    supabase: Client = create_client(url, key)
    
    # Try a simple select. 'courses' table should exist if seeds worked (oh wait seeds failed)
    # Let's try to just get auth settings or a simple query to non-existent table to check connection
    # Or just check if client initializes without error. Client init is lazy, so we need a request.
    
    # Let's try to query 'programs' which might not exist but the request should go through
    response = supabase.table('programs').select("*").limit(1).execute()
    
    print("✅ Connection Successful (REST API)")
    print("Response Data:", response.data)
    
except Exception as e:
    print("\n❌ REST Connection Failed")
    print(str(e))
