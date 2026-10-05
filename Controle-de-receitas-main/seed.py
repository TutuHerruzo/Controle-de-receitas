from app import create_app
from app.database import init_db
from app.models import User

app = create_app()

with app.app_context():
    init_db()
    if not User.find_by_username("admin"):
        User.create("admin", "1234")
        User.create("chef_maria", "receita123")
        print("Usuários criados!")
    else:
        print("Usuários já existentes.")