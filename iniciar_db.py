from app import create_app
from app.database import init_db
from app.models import User

app = create_app()

with app.app_context():
    # 1. Cria as tabelas no banco de dados (incluindo users, recipes e categories)
    init_db()
    
    # 2. Cadastra o usuário de teste padrão exigido pela rubrica
    if not User.find_by_username("admin"):
        # Padrão Active Record correto: Instancia -> Criptografa a Senha -> Salva
        admin = User(username="admin")
        admin.set_password("1234")
        admin.save()
        
        chef = User(username="chef_maria")
        chef.set_password("receita123")
        chef.save()
        
        print("Banco de dados inicializado e usuários de teste criados com sucesso!")
    else:
        print("Os usuários de teste já existem no banco.")