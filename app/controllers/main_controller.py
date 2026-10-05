from flask import Blueprint, render_template, session
from app.middlewares.auth_middleware import login_required
from app.models import Recipe  # <-- NOVO: Importando o model

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def dashboard():
    user_id = session.get('user_id')
    username = session.get('username')
    
    # Busca todas as receitas do usuário (ou você pode usar LIMIT no SQL futuramente para mostrar só as últimas)
    recipes = Recipe.get_all_by_user(user_id)
    
    return render_template('dashboard.html', username=username, recipes=recipes)