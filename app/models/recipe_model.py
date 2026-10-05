from app.database import DBConnection
from datetime import datetime # <-- NOVA IMPORTAÇÃO

class Recipe:
    def __init__(self, user_id, title, description, ingredients, instructions, id=None, created_at=None):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.ingredients = ingredients
        self.instructions = instructions
        
        # Converte para objeto datetime se for string (vem do SQLite)
        if isinstance(created_at, str):
            # O SQLite salva como 'YYYY-MM-DD HH:MM:SS'
            self.created_at = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
        else:
            self.created_at = created_at

    def save(self):
        if self.id is None:
            sql = """
                INSERT INTO recipes (user_id, title, description, ingredients, instructions) 
                VALUES (?, ?, ?, ?, ?)
            """
            with DBConnection() as cursor:
                cursor.execute(sql, (self.user_id, self.title, self.description, self.ingredients, self.instructions))
                self.id = cursor.lastrowid
        else:
            sql = """
                UPDATE recipes 
                SET title = ?, description = ?, ingredients = ?, instructions = ? 
                WHERE id = ? AND user_id = ?
            """
            with DBConnection() as cursor:
                cursor.execute(sql, (self.title, self.description, self.ingredients, self.instructions, self.id, self.user_id))

    def delete(self):
        if self.id is not None:
            sql = "DELETE FROM recipes WHERE id = ? AND user_id = ?"
            with DBConnection() as cursor:
                cursor.execute(sql, (self.id, self.user_id))

    @classmethod
    def get_by_id_and_user(cls, recipe_id: int, user_id: int):
        sql = """
            SELECT id, user_id, title, description, ingredients, instructions, created_at 
            FROM recipes 
            WHERE id = ? AND user_id = ? LIMIT 1
        """
        with DBConnection() as cursor:
            cursor.execute(sql, (recipe_id, user_id))
            row = cursor.fetchone()
            if row:
                return cls(id=row[0], user_id=row[1], title=row[2], description=row[3], 
                           ingredients=row[4], instructions=row[5], created_at=row[6])
        return None

    @classmethod
    def get_all_by_user(cls, user_id: int):
        sql = """
            SELECT id, user_id, title, description, ingredients, instructions, created_at 
            FROM recipes WHERE user_id = ? ORDER BY created_at DESC
        """
        with DBConnection() as cursor:
            cursor.execute(sql, (user_id,))
            rows = cursor.fetchall()
            return [cls(id=r[0], user_id=r[1], title=r[2], description=r[3], 
                        ingredients=r[4], instructions=r[5], created_at=r[6]) for r in rows]