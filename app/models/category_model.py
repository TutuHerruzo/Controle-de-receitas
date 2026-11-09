from app.database import DBConnection

class Category:
    def __init__(self, user_id, name, id=None):
        self.id = id
        self.user_id = user_id
        self.name = name

    def save(self):
        """Salva a categoria no banco (INSERT se nova, UPDATE se já existe)."""
        if self.id is None:
            sql = "INSERT INTO categories (user_id, name) VALUES (?, ?)"
            with DBConnection() as cursor:
                cursor.execute(sql, (self.user_id, self.name))
                self.id = cursor.lastrowid # Atualiza o ID do objeto após inserir
        else:
            sql = "UPDATE categories SET name = ? WHERE id = ? AND user_id = ?"
            with DBConnection() as cursor:
                cursor.execute(sql, (self.name, self.id, self.user_id))

    def delete(self):
        """Remove a categoria garantindo que pertence ao usuário."""
        if self.id is not None:
            sql = "DELETE FROM categories WHERE id = ? AND user_id = ?"
            with DBConnection() as cursor:
                cursor.execute(sql, (self.id, self.user_id))

    @classmethod
    def get_all_by_user(cls, user_id: int):
        """Retorna todas as categorias de um usuário específico."""
        sql = "SELECT id, user_id, name FROM categories WHERE user_id = ? ORDER BY name ASC"
        with DBConnection() as cursor:
            cursor.execute(sql, (user_id,))
            rows = cursor.fetchall()
            # Retorna uma lista de objetos Category instanciados
            return [cls(id=r[0], user_id=r[1], name=r[2]) for r in rows]

    @classmethod
    def get_by_id_and_user(cls, category_id: int, user_id: int):
        """Busca uma categoria específica garantindo segurança de acesso."""
        sql = "SELECT id, user_id, name FROM categories WHERE id = ? AND user_id = ? LIMIT 1"
        with DBConnection() as cursor:
            cursor.execute(sql, (category_id, user_id))
            row = cursor.fetchone()
            if row:
                return cls(id=row[0], user_id=row[1], name=row[2])
        return None