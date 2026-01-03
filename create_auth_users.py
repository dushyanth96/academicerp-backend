"""
Create Supabase Auth users with specific passwords.
This script uses the Supabase Admin API to create authentication users.
"""
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

def create_auth_users():
    # Get Supabase credentials
    url = os.environ.get("SUPABASE_URL")
    # For admin operations, we need the service role key
    # Try SUPABASE_SERVICE_KEY first, fallback to SUPABASE_KEY
    service_key = os.environ.get("SUPABASE_SERVICE_KEY") or os.environ.get("SUPABASE_KEY")
    
    if not url or not service_key:
        print("❌ Error: SUPABASE_URL and SUPABASE_SERVICE_KEY must be set")
        print("   Please add SUPABASE_SERVICE_KEY to your .env file")
        print("   (Find it in Supabase Dashboard > Settings > API > service_role key)")
        return
    
    # Create admin client
    supabase = create_client(url, service_key)
    
    users_to_create = [
        {
            "email": "admin@academicerp.com",
            "password": "admin123",
            "role": "admin",
            "name": "Admin User"
        },
        {
            "email": "faculty@academicerp.com",
            "password": "faculty123",
            "role": "faculty",
            "name": "Dr. Smith"
        }
    ]
    
    print("🔐 Creating Supabase Auth users...\n")
    
    for user_data in users_to_create:
        try:
            # Create auth user with admin API
            auth_response = supabase.auth.admin.create_user({
                "email": user_data["email"],
                "password": user_data["password"],
                "email_confirm": True,  # Auto-confirm email
                "user_metadata": {
                    "name": user_data["name"],
                    "role": user_data["role"]
                }
            })
            
            if auth_response.user:
                supabase_user_id = auth_response.user.id
                print(f"✅ Created auth user: {user_data['email']}")
                print(f"   Supabase User ID: {supabase_user_id}")
                
                # Update faculty_users table with real supabase_user_id
                response = supabase.table('faculty_users').update({
                    'supabase_user_id': supabase_user_id
                }).eq('email', user_data['email']).execute()
                
                if response.data:
                    print(f"   ✅ Linked to faculty_users record\n")
                else:
                    print(f"   ⚠️  Warning: Could not link to faculty_users (record may not exist)\n")
            
        except Exception as e:
            error_msg = str(e)
            
            # Check if user already exists
            if "User already registered" in error_msg or "already registered" in error_msg:
                print(f"⚠️  User {user_data['email']} already exists")
                print(f"   You can reset password in Supabase Dashboard\n")
            elif "service_role" in error_msg or "JWT" in error_msg:
                print(f"❌ Error: Not authorized. You need to use SUPABASE_SERVICE_KEY")
                print(f"   Current key appears to be an 'anon' key, not 'service_role'")
                print(f"   Please update .env with the service_role key from Supabase Dashboard\n")
                break
            else:
                print(f"❌ Error creating {user_data['email']}: {error_msg}\n")
    
    print("\n✨ Auth user creation complete!")
    print("\nYou can now log in with:")
    print("  Admin:   admin@academicerp.com / admin123")
    print("  Faculty: faculty@academicerp.com / faculty123")

if __name__ == "__main__":
    create_auth_users()
