"""
Extract environment variables from .env file for Render deployment.
This script reads your .env and formats it for easy copy-paste to Render.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Environment variables needed for Render
required_vars = [
    'SUPABASE_URL',
    'SUPABASE_KEY',
    'SUPABASE_JWT_SECRET',
    'GEMINI_API_KEY',
    'DATABASE_URL',
    'SUPABASE_SERVICE_KEY'  # Optional but useful for admin operations
]

print("=" * 70)
print("RENDER ENVIRONMENT VARIABLES")
print("=" * 70)
print("\nCopy each variable below and paste into Render Dashboard:\n")

for var in required_vars:
    value = os.environ.get(var)
    if value:
        print(f"✅ {var}")
        print(f"   Value: {value}")
        print()
    else:
        print(f"❌ {var} - NOT FOUND in .env")
        print()

print("=" * 70)
print("\nHOW TO ADD IN RENDER:")
print("1. Go to your Web Service in Render Dashboard")
print("2. Click 'Environment' tab (left sidebar)")
print("3. Click 'Add Environment Variable'")
print("4. Copy Key and Value from above")
print("5. Click 'Save Changes'")
print("6. Repeat for each variable")
print("\nNOTE: Render will automatically restart after you save variables.")
print("=" * 70)
