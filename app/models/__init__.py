from .user_model import User
from .recipe_model import Recipe  # <-- Adicione esta linha

# Exponha ambas as classes
__all__ = ['User', 'Recipe']