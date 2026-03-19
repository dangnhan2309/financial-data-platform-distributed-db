import os
from urllib.parse import quote_plus


def _get_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None or str(value).strip() == "":
        raise ValueError(f"Missing required environment variable: {name}")
    return value


DB_USER = _get_env("ORACLE_USER", "vietfarm_user")
DB_PASSWORD = _get_env("ORACLE_PASSWORD", "GCFood2026")
DB_HOST = _get_env("ORACLE_HOST", "localhost")
DB_PORT = _get_env("ORACLE_PORT", "1521")
DB_SERVICE = _get_env("ORACLE_SERVICE", "FREEPDB1")
DB_ECHO = os.getenv("ORACLE_SQL_ECHO", "false").lower() in {
    "1", "true", "yes", "on"}


def get_sqlalchemy_oracle_url() -> str:
    encoded_password = quote_plus(DB_PASSWORD)
    return (
        f"oracle+oracledb://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/"
        f"?service_name={DB_SERVICE}"
    )


def get_raw_dsn() -> str:
    return f"{DB_HOST}:{DB_PORT}/{DB_SERVICE}"
