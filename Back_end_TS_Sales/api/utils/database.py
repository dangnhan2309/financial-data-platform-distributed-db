import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus

# Load environment variables from .env file
load_dotenv()

# ===== Database Configuration =====
# Oracle Database Connection String
# Format: oracle+oracledb://username:password@host:port/service_name

# Read from environment variables (from .env file)
DB_USER = os.getenv("DB_USER", "gcf_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "123456")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "1521")
DB_SERVICE = os.getenv("DB_SERVICE", "project_db")

# Encode password if it contains special characters
encoded_password = quote_plus(DB_PASSWORD)

# Create Oracle connection string for service_name (not SID)
# Format: oracle+oracledb://user:password@host:port/?service_name=service_name
DATABASE_URL = f"oracle+oracledb://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/?service_name={DB_SERVICE}"

# Create engine with connection pool
engine = create_engine(
    DATABASE_URL,
    # Print SQL statements for debugging
    echo=os.getenv("SQL_ECHO", "false").lower() == "true",
    pool_size=10,  # Number of connections to keep in pool
    max_overflow=20,  # Max connections above pool_size
    pool_pre_ping=True  # Test connections before using
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all ORM models
Base = declarative_base()

# ===== Database Helper Functions =====


def get_db():
    """
    Dependency function to get database session.
    Use this in FastAPI endpoints with: Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        print(f"Database error: {str(e)}")
        raise
    finally:
        db.close()


def init_db():
    """
    Initialize database by creating all tables.
    Call this once when starting the application.
    """
    Base.metadata.create_all(bind=engine)


def drop_db():
    """
    Drop all tables. Use ONLY for testing!
    """
    Base.metadata.drop_all(bind=engine)


def test_connection():
    """
    Test database connection.
    Returns True if connection successful, False otherwise.
    """
    try:
        from sqlalchemy import text
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1 FROM dual"))
            return result.fetchone() is not None
    except Exception as e:
        print(f"Connection failed: {str(e)}")
        return False
