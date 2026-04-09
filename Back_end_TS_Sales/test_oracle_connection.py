"""
Quick Oracle Connection Test for GCFood_Project

Run with:
    python test_oracle_connection.py

This script tests the Oracle connection with your GCFood_Project credentials.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import text

# Load environment variables from .env file
load_dotenv()

print("=" * 70)
print("GC Food - Oracle Connection Test")
print("=" * 70)

# Get credentials from .env
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_service = os.getenv("DB_SERVICE")

print("\n📋 Configuration Loaded:")
print(f"   User: {db_user}")
print(f"   Host: {db_host}")
print(f"   Port: {db_port}")
print(f"   Service: {db_service}")

print("\n🔍 Attempting to connect to Oracle...\n")

try:
    # Import after showing config
    from api.utils.database import test_connection, engine, SessionLocal

    # Test basic connection
    if test_connection():
        print("✅ CONNECTION SUCCESSFUL!")
        print("   Oracle server is reachable and responding")

        # Try to create and use a session
        try:
            db = SessionLocal()
            print("✅ SESSION CREATED!")
            print("   Database session opened successfully")

            # Try a simple query (use text() for raw SQL in SQLAlchemy 2.0+)
            result = db.execute(text("SELECT 1 FROM dual"))
            data = result.fetchone()
            print("✅ QUERY EXECUTED!")
            print("   Test query 'SELECT 1 FROM dual' returned:", data)

            db.close()
            print("✅ SESSION CLOSED!")
            print("   Database session closed successfully")

            print("\n" + "=" * 70)
            print("🎉 ALL TESTS PASSED - Oracle is ready to use!")
            print("=" * 70)
            print("\nYou can now:")
            print("   1. Run: python run.py")
            print("   2. Visit: http://localhost:8000/docs")
            print("   3. Create models and API endpoints")

        except Exception as e:
            print(f"\n❌ Session Error: {str(e)}")
            print("\nTroubleshooting:")
            print("   1. Check if GCFood_Project service is running")
            print("   2. Verify credentials in .env file")
            print("   3. Try connecting with SQL Developer")

    else:
        print("❌ CONNECTION FAILED!")
        print("\nPossible causes:")
        print("   1. Oracle service is not running")
        print("   2. Wrong hostname/port/service name")
        print("   3. Wrong username/password")
        print("   4. Network/firewall issue")

        print("\n🔧 Troubleshooting steps:")
        print("   1. Check .env file has correct values:")
        print(f"      DB_USER={db_user}")
        print(f"      DB_HOST={db_host}")
        print(f"      DB_PORT={db_port}")
        print(f"      DB_SERVICE={db_service}")
        print("\n   2. Test with SQL Developer or SQL*Plus:")
        print(f"      sqlplus {db_user}/@{db_host}:{db_port}/{db_service}")
        print("\n   3. Check Oracle listener is running:")
        print("      lsnrctl status")

except ImportError as e:
    print(f"❌ Import Error: {str(e)}")
    print("\nRequired packages are missing. Install with:")
    print("   pip install python-oracledb sqlalchemy python-dotenv")

except Exception as e:
    print(f"❌ Unexpected Error: {str(e)}")
    print("\nCheck your Oracle configuration and try again.")
