from werkzeug.security import generate_password_hash, check_password_hash
from app.database import DBConnection

class User:
    def __init__(self, username, password_hash=None, id=None, created_at=None):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.created_at = created_at

    def set_password(self, password: str):
        """Criptografa a senha em texto plano e a atribui à instância."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verifica se a senha em texto plano bate com o hash da instância."""
        return check_password_hash(self.password_hash, password)

    def save(self):
        """Salva a instância atual no banco (INSERT se novo, UPDATE se já existe)."""
        if self.id is None:
            sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
            with DBConnection() as cursor:
                cursor.execute(sql, (self.username, self.password_hash))
                self.id = cursor.lastrowid # Preenche o ID após a inserção
        else:
            sql = "UPDATE users SET username = ?, password_hash = ? WHERE id = ?"
            with DBConnection() as cursor:
                cursor.execute(sql, (self.username, self.password_hash, self.id))

    def delete(self):
        """Remove a instância atual do banco de dados."""
        if self.id is not None:
            sql = "DELETE FROM users WHERE id = ?"
            with DBConnection() as cursor:
                cursor.execute(sql, (self.id,))

    @classmethod
    def find_by_username(cls, username: str):
        sql = "SELECT id, username, password_hash, created_at FROM users WHERE username = ? LIMIT 1"
        with DBConnection() as cursor:
            cursor.execute(sql, (username,))
            row = cursor.fetchone()
            if row:
                # Retorna uma nova instância populada com os dados do banco
                return cls(id=row[0], username=row[1], password_hash=row[2], created_at=row[3])
        return None

    @classmethod
    def find_by_id(cls, user_id: int):
        sql = "SELECT id, username, password_hash, created_at FROM users WHERE id = ? LIMIT 1"
        with DBConnection() as cursor:
            cursor.execute(sql, (user_id,))
            row = cursor.fetchone()
            if row:
                return cls(id=row[0], username=row[1], password_hash=row[2], created_at=row[3])
        return None

    @classmethod
    def authenticate(cls, username: str, password: str):
        user = cls.find_by_username(username)
        if user and user.check_password(password):
            return user
        return None