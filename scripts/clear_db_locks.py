from src.fetch_data import get_db_connection
from sqlalchemy import text

engine = get_db_connection()
with engine.connect() as conn:
    # Find active pids
    res = conn.execute(text("SELECT pid, state, query FROM pg_stat_activity WHERE datname = 'mutualfunds' AND pid <> pg_backend_pid()"))
    for row in res.fetchall():
        print(row)
        pid = row[0]
        conn.execute(text(f"SELECT pg_terminate_backend({pid})"))
        print(f"Terminated {pid}")
