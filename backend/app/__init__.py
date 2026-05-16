from flask import Flask
from .models import db
from .schemas import ma

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    
    db.init_app(app)
    ma.init_app(app)

    from .routes import bp
    app.register_blueprint(bp)

    return app