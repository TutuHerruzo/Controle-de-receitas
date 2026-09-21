from werkzeug.security import generate_password_hash, check_password_hash

# Dicionário armazenando as senhas já criptografadas com hash
USERS_DB = {
    "admin": generate_password_hash("1234"),
    "chef_maria": generate_password_hash("receita123"),
    "gastronomo": generate_password_hash("senha123")
}

class User:
    def __init__(self, username):
        self.username = username

    @staticmethod
    def authenticate(username, password):
        """
        Verifica se o usuário existe e se a hash da senha confere.
        """
        if username in USERS_DB:
            stored_hash = USERS_DB[username]
            if check_password_hash(stored_hash, password):
                return User(username)
        return None