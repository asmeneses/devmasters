import os

class Config:
    SECRET_TOKEN = 'my_static_token'  # Definición token estático

    # Configuración para la base de datos en AWS RDS
    SQLALCHEMY_DATABASE_URI = (
         f'postgresql://{os.getenv("DB_USERNAME", "")}:{os.getenv("DB_PASSWORD", "")}@'
         f'{os.getenv("DB_HOST", "")}/{os.getenv("DB_NAME", "")}'
     )
    
    if SQLALCHEMY_DATABASE_URI == "postgresql://:@/":
        SQLALCHEMY_DATABASE_URI = 'sqlite:///blacklist.db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

