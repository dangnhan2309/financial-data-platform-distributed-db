from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from api.utils.oracle_settings import DB_ECHO, get_sqlalchemy_oracle_url


SQLALCHEMY_DATABASE_URL = get_sqlalchemy_oracle_url()

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=DB_ECHO,
    pool_pre_ping=True,
    pool_recycle=1800,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()
