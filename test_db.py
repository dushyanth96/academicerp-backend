import os
import urllib.parse
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load env variables
load_dotenv()

def test_connection():
    db_url = os.getenv('DATABASE_URL')
    print(f"Testing Connection to: {db_url}")
    
    if not db_url:
        print("❌ DATABASE_URL is not set in .env")
        return

    # Create engine
    try:
        engine = create_engine(db_url)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ SUCCESS! Connected to:")
            print(f"   {version}")
    except Exception as e:
        print("\n❌ CONNECTION FAILED")
        print("Error Details:")
        print(str(e))
        print("\nPossible causes:")
        print("1. Incorrect Password")
        print("2. Database 'postgres' does not exist")
        print("3. Firewall/Network blocking blocking port 5432")
        print("4. Hostname typo")

if __name__ == "__main__":
    test_connection()
