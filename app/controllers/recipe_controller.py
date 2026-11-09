from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models import Recipe
from app.middlewares.auth_middleware import login_required
from app.models.category_model import Category

recipe_bp = Blueprint('recipe', __name__, url_prefix='/recipes')

@recipe_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_recipe():
    user_id = session.get('user_id')
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        ingredients = request.form.get('ingredients', '').strip()
        instructions = request.form.get('instructions', '').strip()
        category_id = request.form.get('category_id') # Captura a categoria selecionada
        
        # Converte para int se houver valor, senão None
        category_id = int(category_id) if category_id else None

        if not title or not ingredients or not instructions:
            flash('Título, ingredientes e modo de preparo são obrigatórios.', 'warning')
            categorias = Category.get_all_by_user(user_id)
            return render_template('form.html', categories=categorias)

        nova_receita = Recipe(
            user_id=user_id,
            category_id=category_id,
            title=title,
            description=description,
            ingredients=ingredients,
            instructions=instructions
        )
        nova_receita.save()
        
        flash('Receita criada com sucesso!', 'success')
        return redirect(url_for('main.dashboard'))

    # Para GET, buscamos as categorias para preencher o select do HTML
    categorias = Category.get_all_by_user(user_id)
    return render_template('form.html', categories=categorias)


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

# Adicione no final de recipe_controller.py

@recipe_bp.route('/view/<int:id>')
@login_required
def view_recipe(id):
    # Busca a receita garantindo que pertence ao usuário logado
    recipe = Recipe.get_by_id_and_user(id, session.get('user_id'))
    
    if not recipe:
        flash('Receita não encontrada.', 'danger')
        return redirect(url_for('main.dashboard'))
        
    return render_template('recipe_detail.html', recipe=recipe)


@recipe_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_recipe(id):
    # 1. Busca a receita no banco
    recipe = Recipe.get_by_id_and_user(id, session.get('user_id'))
    
    if not recipe:
        flash('Receita não encontrada.', 'danger')
        return redirect(url_for('main.dashboard'))
        
    # 2. Se for POST (clicou no botão Salvar)
    if request.method == 'POST':
        recipe.title = request.form.get('title', '').strip()
        recipe.description = request.form.get('description', '').strip()
        recipe.ingredients = request.form.get('ingredients', '').strip()
        recipe.instructions = request.form.get('instructions', '').strip()
        
        if not recipe.title or not recipe.ingredients or not recipe.instructions:
            flash('Título, ingredientes e modo de preparo são obrigatórios.', 'warning')
            return render_template('form.html', recipe=recipe)
            
        # Como a receita JÁ TEM ID, esse save() vai fazer um UPDATE inteligente!
        recipe.save() 
        flash('Receita atualizada com sucesso!', 'success')
        return redirect(url_for('recipe.view_recipe', id=recipe.id))
        
    # 3. Se for GET (apenas abriu a tela), desenha o formulário com os dados velhos
    return render_template('form.html', recipe=recipe)

    