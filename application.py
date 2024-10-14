from flask import Flask
from models import db
from config import Config


application = Flask(__name__)
application.config.from_object(Config)

db.init_app(application)

from views import *  

if __name__ == '__main__':
    with application.app_context():
        db.create_all()
    application.run(debug=True)
