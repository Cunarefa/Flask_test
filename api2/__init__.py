import os

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
ma = Marshmallow()
login_manager = LoginManager()
jwt = JWTManager()
migrate = Migrate()

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Actimel13@localhost:5433/avada2'

    db.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    from api2.blueprints import bp_api, bp_auth

    app.register_blueprint(bp_api, url_prefix='/api')
    app.register_blueprint(bp_auth, url_prefix='/auth')

    return app

