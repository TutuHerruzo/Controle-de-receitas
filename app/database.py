import os
from sqlalchemy import create_engine

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///database.db')

# O SQLAlchemy atua APENAS como pool e engine de conexão
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=False
)

class DBConnection:
    """
    Gerenciador de contexto seguro para conexões com o banco de dados.
    Garante commit em caso de sucesso e rollback em caso de falha.
    """
    def __init__(self):
        self.raw_conn = engine.raw_connection()
        self.cursor = None

    def __enter__(self):
        self.cursor = self.raw_conn.cursor()
        # Necessário no SQLite nativo para validar exclusões em cascata (FOREIGN KEYS)
        self.cursor.execute("PRAGMA foreign_keys = ON;")
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is None:
                self.raw_conn.commit()  # Sucesso: salva as alterações
            else:
                self.raw_conn.rollback()  # Erro: desfaz a transação
        finally:
            if self.cursor:
                self.cursor.close()
            if self.raw_conn:
                self.raw_conn.close()
        # Retornar False garante que exceções não sejam silenciadas e subam para a aplicação
        return False

def init_db():
    create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """
    create_users_index = "CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);"
    
    create_recipes_table = """
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            ingredients TEXT NOT NULL,
            instructions TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """
    create_recipes_index = "CREATE INDEX IF NOT EXISTS idx_recipes_user_id ON recipes(user_id);"

    with DBConnection() as cursor:
        cursor.execute(create_users_table)
        cursor.execute(create_users_index)
        cursor.execute(create_recipes_table)
        cursor.execute(create_recipes_index)