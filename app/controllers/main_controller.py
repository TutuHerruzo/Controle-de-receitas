from flask import Blueprint, render_template, session, request # <-- Adicionado o request
from app.middlewares.auth_middleware import login_required
from app.models import Recipe 
from app.models.category_model import Category 
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def dashboard():
    user_id = session.get('user_id')
    username = session.get('username')
    
    # Captura os filtros da URL (busca por texto e ID da categoria)
    busca = request.args.get('busca', '')
    categoria_id = request.args.get('categoria', type=int)
    pagina = request.args.get('pagina', 1, type=int)
    
    # Busca as receitas filtrando por usuário, nome e categoria
    recipes = Recipe.get_dynamic_list(user_id, search=busca, category_id=categoria_id, page=pagina, per_page=6)
    
    # Busca todas as categorias para preencher o filtro na barra de pesquisa do dashboard
    categorias = Category.get_all_by_user(user_id)
    
    return render_template('dashboard.html', 
                           username=username, 
                           recipes=recipes, 
                           busca=busca, 
                           categoria_selecionada=categoria_id,
                           categorias=categorias,
                           pagina=pagina)