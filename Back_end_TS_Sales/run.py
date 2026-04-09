"""
Entry point for GC Food TS Sales Backend API

Run the server with:
    python run.py

The API will be available at:
    http://localhost:8000
    
API Documentation:
    http://localhost:8000/docs (Swagger UI)
    http://localhost:8000/redoc (ReDoc UI)
"""

import uvicorn
import os
from api.utils.database import test_connection


def main():
    """Main entry point."""

    # Test database connection first
    print("🔍 Testing database connection...")
    if test_connection():
        print("✅ Database connection successful")
    else:
        print("❌ Database connection failed. Check your credentials and Oracle instance.")
        print(f"   Check your .env file or environment variables:")
        print(f"   DB_USER={os.getenv('DB_USER', 'ts_sales')}")
        print(f"   DB_HOST={os.getenv('DB_HOST', 'localhost')}")
        print(f"   DB_PORT={os.getenv('DB_PORT', '1521')}")
        print(f"   DB_SERVICE={os.getenv('DB_SERVICE', 'orcl')}")
        return

    # Start API server
    print("\n🚀 Starting GC Food TS Sales API...")
    print("📍 API will run at: http://localhost:8001")
    print("📚 Swagger Docs: http://localhost:8001/docs")
    print("📖 ReDoc: http://localhost:8001/redoc")
    print("\n⏹️  Press Ctrl+C to stop the server\n")

    uvicorn.run(
        "api.main:app",
        host="127.0.0.1",  # Changed from 0.0.0.0 to 127.0.0.1 (localhost)
        port=8001,  # Changed to 8001 due to port 8000 conflicts
        reload=False,  # Changed to False temporarily to fix email-validator subprocess issue
        log_level="info"
    )


if __name__ == "__main__":
    main()
