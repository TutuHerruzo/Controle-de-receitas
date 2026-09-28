import os
from contextlib import contextmanager
from sqlalchemy import create_engine

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///database.db')

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=False
)

@contextmanager
def get_db_cursor():
    """
    Gerenciador de contexto que fornece um cursor nativo (DBAPI).
    Garante commit, rollback e encerramento correto do cursor e conexão.
    """
    raw_conn = engine.raw_connection()
    cursor = raw_conn.cursor()
    try:
        yield cursor
        raw_conn.commit()
    except Exception:
        raw_conn.rollback()
        raise
    finally:
        cursor.close()
        raw_conn.close()

def init_db():
    """Cria tabelas e índices executando DDL diretamente pelo cursor."""
    create_table_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """
    create_index_sql = """
        CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
    """
    with get_db_cursor() as cursor:
        cursor.execute(create_table_sql)
        cursor.execute(create_index_sql)