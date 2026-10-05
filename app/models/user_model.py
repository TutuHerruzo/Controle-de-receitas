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
        sql = """
            SELECT id, username, password_hash, created_at 
            FROM users 
            WHERE username = ? 
            LIMIT 1
        """
        with get_db_cursor() as cursor:
            cursor.execute(sql, (username,))
            row = cursor.fetchone()
            if row:
                return cls(
                    id=row[0],
                    username=row[1],
                    password_hash=row[2],
                    created_at=row[3]
                )
        return None

    @classmethod
    def create(cls, username: str, password: str):
        password_hash = generate_password_hash(password)
        sql = """
            INSERT INTO users (username, password_hash) 
            VALUES (?, ?)
        """
        with get_db_cursor() as cursor:
            cursor.execute(sql, (username, password_hash))

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @classmethod
    def authenticate(cls, username: str, password: str):
        user = cls.find_by_username(username)
        if user and user.check_password(password):
            return user
        return None