from flask import Blueprint, render_template, request, redirect, url_for, session, flash, make_response, current_app
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
            
            # --- REGISTRO DE LOG DE SUCESSO ---
            current_app.logger.info(f"O usuário '{user.username}' realizou login no sistema.")
            
            resposta = make_response(redirect(url_for('main.dashboard')))
            resposta.set_cookie('last_username', username, max_age=60*60*24*7)
            return resposta
            
        else:
            flash('Usuário ou senha incorretos!', 'danger')
            
            # --- REGISTRO DE LOG DE FALHA ---
            current_app.logger.warning(f"Tentativa de login falha para o usuário: '{username}'.")

    # --- 3. LEITURA DO COOKIE ---
    # Quando for requisição GET, tenta ler o cookie do navegador. Se não existir, fica vazio ('').
    ultimo_user = request.cookies.get('last_username', '')
    
    # Enviamos a variável last_user para o HTML preencher o input
    return render_template('login.html', last_user=ultimo_user)

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