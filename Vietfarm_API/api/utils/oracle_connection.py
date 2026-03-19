import os
import subprocess
import sys

try:
    import oracledb
except ModuleNotFoundError:
    script_path = os.path.abspath(__file__)
    venv_python = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..",
                     "..", ".venv", "Scripts", "python.exe")
    )

    if os.path.exists(venv_python) and os.path.abspath(sys.executable) != venv_python:
        print(f"[INFO] oracledb not found in {sys.executable}")
        print(
            f"[INFO] Re-running with workspace virtual environment: {venv_python}")
        result = subprocess.run([venv_python, script_path], check=False)
        raise SystemExit(result.returncode)

    print(
        f"[ERROR] Missing package 'oracledb' in interpreter: {sys.executable}")
    print("[HINT] Install package with: py -m pip install oracledb")
    raise SystemExit(1)

if __package__ in {None, ""}:
    # Allow running this file directly: python oracle_connection.py
    sys.path.insert(0, os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")))

from api.utils.oracle_settings import DB_HOST, DB_PASSWORD, DB_PORT, DB_SERVICE, DB_USER, get_raw_dsn


def get_oracle_connection() -> oracledb.Connection:
    return oracledb.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        dsn=get_raw_dsn(),
    )


def test_oracle_connection() -> dict:
    try:
        with get_oracle_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 'Connection OK' FROM DUAL")
                row = cursor.fetchone()

        return {
            "database_status": "Connected",
            "oracle_response": row[0] if row else None,
            "host": DB_HOST,
            "port": DB_PORT,
            "service_name": DB_SERVICE,
            "user": DB_USER,
        }
    except oracledb.Error as exc:
        return {
            "database_status": "Disconnected",
            "error": str(exc),
            "host": DB_HOST,
            "port": DB_PORT,
            "service_name": DB_SERVICE,
            "user": DB_USER,
        }


if __name__ == "__main__":
    result = test_oracle_connection()
    if result.get("database_status") == "Connected":
        print(f"[OK] Oracle connected: {result}")
        raise SystemExit(0)

    print(f"[FAIL] Oracle connection failed: {result}")
    raise SystemExit(1)
