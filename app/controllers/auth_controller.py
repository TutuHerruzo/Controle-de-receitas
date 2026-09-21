from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # 🔒 SE O USUÁRIO JÁ ESTIVER LOGADO: Redireciona para o dashboard
    if 'user' in session:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.authenticate(username, password)

        if user:
            session['user'] = user.username
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Usuário ou senha incorretos!', 'danger')

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('auth.login'))