from app import create_app
from app.database import init_db

app = create_app()

# Garante a criação da tabela e índices via SQL puro na inicialização
with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(debug=True)