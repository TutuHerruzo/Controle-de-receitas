from flask import Flask
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__, template_folder='views')
    app.config.from_object(config_class)

    # Registra Blueprints
    from app.controllers.auth_controller import auth_bp
    from app.controllers.main_controller import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app