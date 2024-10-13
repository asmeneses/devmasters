import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///blacklist.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_TOKEN = 'my_static_token'  # Definición token estático
