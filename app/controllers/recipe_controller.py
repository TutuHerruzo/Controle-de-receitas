from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models import Recipe
from app.middlewares.auth_middleware import login_required

recipe_bp = Blueprint('recipe', __name__, url_prefix='/recipes')

@recipe_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_recipe():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        ingredients = request.form.get('ingredients', '').strip()
        instructions = request.form.get('instructions', '').strip()
        
        if not title or not ingredients or not instructions:
            flash('Título, ingredientes e modo de preparo são obrigatórios.', 'warning')
            return render_template('recipes/form.html')

        # Usando o padrão Active Record que criamos
        nova_receita = Recipe(
            user_id=session.get('user_id'),
            title=title,
            description=description,
            ingredients=ingredients,
            instructions=instructions
        )
        nova_receita.save()
        
        flash('Receita criada com sucesso!', 'success')
        # Redireciona para o dashboard conforme combinamos
        return redirect(url_for('main.dashboard'))

    return render_template('form.html')

@recipe_bp.route('/<int:recipe_id>/delete', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    user_id = session.get('user_id')
    
    # Busca a receita garantindo que pertence ao usuário logado
    receita = Recipe.get_by_id_and_user(recipe_id, user_id)
    if receita:
        receita.delete()
        flash('Receita excluída com sucesso!', 'info')
    else:
        flash('Receita não encontrada ou você não tem permissão para excluí-la.', 'danger')
        
    return redirect(url_for('main.dashboard'))