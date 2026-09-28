from app import create_app
from app.database import init_db
from app.models import User

app = create_app()

with app.app_context():
    # 1. Garante a criação da tabela e índices
    init_db()

    # 2. Insere os usuários com senhas criptografadas
    if not User.find_by_username("admin"):
        User.create("admin", "1234")
        User.create("chef_maria", "receita123")
        User.create("Arthur", "12345")
        print("✅ Usuários 'admin' e 'chef_maria' criados com sucesso!")
    else:
        print("ℹ️ Usuários já existentes no banco.")