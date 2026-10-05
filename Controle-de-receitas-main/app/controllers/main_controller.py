from flask import Blueprint, render_template, session
from app.middlewares.auth_middleware import login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def dashboard():
    username = session.get('username')
    return render_template('dashboard.html', username=username)