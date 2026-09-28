from werkzeug.security import generate_password_hash, check_password_hash
from app.database import get_db_cursor

class User:
    def __init__(self, id, username, password_hash, created_at=None):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.created_at = created_at

    @classmethod
    def find_by_username(cls, username: str):
        """
        Busca um usuário via SELECT parametrizado com cursor.
        Protegido contra SQL Injection via tupla (username,).
        """
        sql = """
            SELECT id, username, password_hash, created_at 
            FROM users 
            WHERE username = ? 
            LIMIT 1
        """
        with get_db_cursor() as cursor:
            # O segundo argumento DEVE ser uma tupla (username,)
            cursor.execute(sql, (username,))
            row = cursor.fetchone()
            
            if row:
                # O cursor do SQLite retorna uma tupla posicional: (id, username, password_hash, created_at)
                return cls(
                    id=row[0],
                    username=row[1],
                    password_hash=row[2],
                    created_at=row[3]
                )
        return None

    @classmethod
    def create(cls, username: str, password: str):
        """
        Insere um novo usuário via INSERT parametrizado com cursor.
        """
        password_hash = generate_password_hash(password)
        sql = """
            INSERT INTO users (username, password_hash) 
            VALUES (?, ?)
        """
        with get_db_cursor() as cursor:
            # Passagem segura dos dois valores
            cursor.execute(sql, (username, password_hash))

    def check_password(self, password: str) -> bool:
        """Valida a senha fornecida comparando com o hash salvo."""
        return check_password_hash(self.password_hash, password)

    @classmethod
    def authenticate(cls, username: str, password: str):
        """Verifica se o usuário existe e valida sua senha."""
        user = cls.find_by_username(username)
        if user and user.check_password(password):
            return user
        return None
    

