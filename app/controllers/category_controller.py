from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from app.models.category_model import Category  # Ajuste o import se o seu arquivo tiver outro nome ou caminho
from app.middlewares.auth_middleware import login_required

category_bp = Blueprint('category', __name__, url_prefix='/categories')

@category_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    user_id = session.get('user_id')

    # Fluxo de Cadastro (CREATE) via POST
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        
        if not name:
            flash('O nome da categoria é obrigatório.', 'warning')
        else:
            # Instancia o Model da Categoria e salva
            nova_categoria = Category(user_id=user_id, name=name)
            nova_categoria.save()
            
            # Log de eventos obrigatório do projeto
            current_app.logger.info(f"O usuário ID {user_id} criou a categoria '{name}'.")
            flash('Categoria criada com sucesso!', 'success')
            
        return redirect(url_for('category.index'))

    # Fluxo de Listagem (READ) via GET
    categorias = Category.get_all_by_user(user_id)
    return render_template('categories.html', categorias=categorias)


@category_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_category(id):
    # Fluxo de Exclusão (DELETE) seguro validando o dono do registro
    user_id = session.get('user_id')
    categoria = Category.get_by_id_and_user(id, user_id)

    if categoria:
        categoria.delete()
        # Log de exclusão obrigatório do projeto
        current_app.logger.info(f"O usuário ID {user_id} excluiu a categoria ID {id}.")
        flash('Categoria excluída com sucesso!', 'info')
    else:
        flash('Categoria não encontrada ou você não tem permissão para excluí-la.', 'danger')

    return redirect(url_for('category.index'))