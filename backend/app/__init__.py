import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv # Adicione esta linha
from .models import db
from .schemas import ma

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    ma.init_app(app)

    from .routes import bp
    app.register_blueprint(bp)
    return app