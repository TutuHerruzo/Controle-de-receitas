from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Se já estiver logado, redireciona para o painel principal
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        # O método authenticate continua sendo um @classmethod que retorna uma instância ou None
        user = User.authenticate(username, password)

        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Usuário ou senha incorretos!', 'danger')

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Se já estiver logado, redireciona para o painel principal
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not username or not password:
            flash('Preencha todos os campos!', 'warning')
        elif password != confirm_password:
            flash('As senhas não coincidem!', 'danger')
        elif User.find_by_username(username):
            flash('Este nome de usuário já está cadastrado!', 'danger')
        else:
            # NOVO PADRÃO ACTIVE RECORD: Instancia, prepara e salva.
            novo_usuario = User(username=username)
            novo_usuario.set_password(password)
            novo_usuario.save()
            
            flash('Conta criada com sucesso! Faça login para continuar.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('auth.login'))