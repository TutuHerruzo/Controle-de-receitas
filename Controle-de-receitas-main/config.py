import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'chave_secreta_super_segura_dev_123')