from flask import Flask
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
ma = Marshmallow()
login = LoginManager()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Actimel13@localhost:5433/avada2'

    db.init_app(app)
    ma.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db)

    from api2.blueprints import bp_api

    app.register_blueprint(bp_api, url_prefix='/api')

    return app

