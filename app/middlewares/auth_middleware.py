from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    """
    Decorator que exige autenticação para acessar a rota decorada.
    Preserva a assinatura original da função decorada com @wraps.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Por favor, faça login para acessar esta página.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function