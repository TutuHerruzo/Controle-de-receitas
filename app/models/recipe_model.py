from app.database import DBConnection
from datetime import datetime # <-- NOVA IMPORTAÇÃO

class Recipe:
    def __init__(self, user_id, title, description, ingredients, instructions, category_id=None, id=None, created_at=None, category_name=None):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.ingredients = ingredients
        self.instructions = instructions
        self.category_id = category_id
        self.created_at = created_at
        self.category_name = category_name  # Útil para exibir o nome na tela

    def save(self):
        if self.id is None:
            sql = """
                INSERT INTO recipes (user_id, category_id, title, description, ingredients, instructions) 
                VALUES (?, ?, ?, ?, ?, ?)
            """
            with DBConnection() as cursor:
                cursor.execute(sql, (self.user_id, self.category_id, self.title, self.description, self.ingredients, self.instructions))
                self.id = cursor.lastrowid
        else:
            sql = """
                UPDATE recipes 
                SET category_id = ?, title = ?, description = ?, ingredients = ?, instructions = ? 
                WHERE id = ? AND user_id = ?
            """
            with DBConnection() as cursor:
                cursor.execute(sql, (self.category_id, self.title, self.description, self.ingredients, self.instructions, self.id, self.user_id))

    def delete(self):
        if self.id is not None:
            sql = "DELETE FROM recipes WHERE id = ? AND user_id = ?"
            with DBConnection() as cursor:
                cursor.execute(sql, (self.id, self.user_id))

    @classmethod
    def get_by_id_and_user(cls, recipe_id: int, user_id: int):
        """Busca uma receita específica garantindo que pertence ao usuário logado."""
        sql = """
            SELECT id, user_id, category_id, title, description, ingredients, instructions, created_at 
            FROM recipes 
            WHERE id = ? AND user_id = ? LIMIT 1
        """
        with DBConnection() as cursor:
            cursor.execute(sql, (recipe_id, user_id))
            row = cursor.fetchone()
            if row:
                # Instancia a receita com os dados retornados do banco
                recipe = cls(
                    id=row['id'],
                    user_id=row['user_id'],
                    category_id=row['category_id'],
                    title=row['title'],
                    description=row['description'],
                    ingredients=row['ingredients'],
                    instructions=row['instructions'],
                    created_at=row['created_at']
                )
                return recipe
        return None
    
    @classmethod
    def get_dynamic_list(cls, user_id, search='', category_id=None, page=1, per_page=6):
        offset = (page - 1) * per_page
        search_term = f"%{search}%"
        
        # Montamos a query unindo (LEFT JOIN) com a tabela de categorias para pegar o nome dela
        sql = """
            SELECT r.id, r.user_id, r.category_id, r.title, r.description, 
                   r.ingredients, r.instructions, r.created_at, c.name as category_name
            FROM recipes r
            LEFT JOIN categories c ON r.category_id = c.id
            WHERE r.user_id = ? AND r.title LIKE ?
        """
        params = [user_id, search_term]
        
        # Se o usuário filtrou por uma categoria específica, adicionamos no WHERE
        if category_id:
            sql += " AND r.category_id = ?"
            params.append(category_id)
            
        sql += " ORDER BY r.id DESC LIMIT ? OFFSET ?"
        params.extend([per_page, offset])
        
        with DBConnection() as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            
            recipes = []
            for row in rows:
                recipe = cls(
                    id=row['id'],
                    user_id=row['user_id'],
                    category_id=row['category_id'],
                    title=row['title'],
                    description=row['description'],
                    ingredients=row['ingredients'],
                    instructions=row['instructions'],
                    created_at=row['created_at'],
                    category_name=row['category_name']
                )
                recipes.append(recipe)
                
            return recipes