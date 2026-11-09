from functools import wraps
from flask import session, redirect, url_for, flash, g
from app.models import User # <-- Importamos o User model que você acabou de mostrar!

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 1. Verifica se o usuário tem a sessão ativa
        user_id = session.get('user_id')
        if not user_id:
            flash('Por favor, faça login para acessar esta página.', 'warning')
            return redirect(url_for('auth.login'))
            
        # 2. Busca o usuário no banco (Requisito do projeto!)
        usuario_logado = User.find_by_id(user_id)
        
        if not usuario_logado:
            # Se o ID está na sessão mas não existe no banco, limpa a sessão falsa
            session.clear()
            flash('Usuário não encontrado. Faça login novamente.', 'danger')
            return redirect(url_for('auth.login'))
            
        # 3. Disponibiliza o usuário no objeto 'g' do Flask (Requisito do projeto!)
        g.usuario = usuario_logado
        
        return f(*args, **kwargs)
    return decorated_function