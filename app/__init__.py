import os
from flask import Flask
from app.controllers import auth_bp, main_bp

def create_app():
    views_path = os.path.join(os.path.dirname(__file__), 'views')

    app = Flask(__name__, template_folder=views_path)
    app.secret_key = 'sua_chave_secreta_super_segura_aqui'

    # Registrar os Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app