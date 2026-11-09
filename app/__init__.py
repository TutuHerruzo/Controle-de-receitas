from flask import Flask, render_template # <-- ADICIONE O render_template AQUI
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__, template_folder='views')
    app.config.from_object(config_class)

    # Importando os Blueprints
    from app.controllers.auth_controller import auth_bp
    from app.controllers.main_controller import main_bp
    from app.controllers.recipe_controller import recipe_bp
    from app.controllers.category_controller import category_bp

    # Registrando os Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(recipe_bp)
    app.register_blueprint(category_bp)

    # --- TRATAMENTO DE ERRO 404 (Requisito do Projeto) ---
    @app.errorhandler(404)
    def page_not_found(e):
        # O Flask passará o erro 'e' automaticamente. Retornamos a view e o status 404.
        return render_template('404.html'), 404

    return app