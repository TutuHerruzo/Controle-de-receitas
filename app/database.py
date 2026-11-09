import sqlite3
import os

# Define o caminho do banco nativo na pasta do projeto (Padrão Aula 15)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_URL = os.path.join(BASE_DIR, 'database.db')

class DBConnection:
    """
    Gerenciador de contexto seguro para conexões com o banco de dados.
    Garante commit em caso de sucesso e rollback em caso de falha.
    """
    def __init__(self, db_path=DATABASE_URL):
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def __enter__(self):
        # Usando o sqlite3 nativo exigido pelo documento
        self.conn = sqlite3.connect(self.db_path)
        
        # Ativa o row_factory (Requisito da Aula 15)
        # Bônus: Ele permite que as suas tuplas (row[0]) continuem funcionando!
        self.conn.row_factory = sqlite3.Row 
        
        self.cursor = self.conn.cursor()
        
        # Necessário no SQLite nativo para validar exclusões em cascata (FOREIGN KEYS)
        self.cursor.execute("PRAGMA foreign_keys = ON;")
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is None:
                self.conn.commit()  # Sucesso: salva as alterações
            else:
                self.conn.rollback()  # Erro: desfaz a transação
        finally:
            # O SQLite nativo não precisa de cursor.close(), apenas fechar a conexão
            if self.conn:
                self.conn.close()
        # Retornar False garante que exceções subam para a aplicação
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

    create_recipes_table = """
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category_id INTEGER,  -- <--- NOVA COLUNA
            title TEXT NOT NULL,
            description TEXT,
            ingredients TEXT NOT NULL,
            instructions TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
        );
    """

    create_recipes_index = "CREATE INDEX IF NOT EXISTS idx_recipes_user_id ON recipes(user_id);"

    # --- AQUI ENTRA A SEGUNDA ENTIDADE DO PROJETO: CATEGORIAS ---
    create_categories_table = """
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """

    with DBConnection() as cursor:
        cursor.execute(create_users_table)
        cursor.execute(create_users_index)
        
        cursor.execute(create_recipes_table)
        cursor.execute(create_recipes_index)
        
        # Executando a criação da tabela de categorias
        cursor.execute(create_categories_table)