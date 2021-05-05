import os

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, current_user
from flask_principal import Principal, Permission, RoleNeed, identity_loaded, UserNeed
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ma = Marshmallow()
login_manager = LoginManager()
jwt = JWTManager()
migrate = Migrate()
principals = Principal()

load_dotenv()

admin_permission = Permission(RoleNeed('admin'))


def create_app():
    app = Flask(__name__)

    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

    db.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    principals.init_app(app)

    from api2.blueprints import bp_api, bp_auth, like_api, comment_api

    app.register_blueprint(bp_api, url_prefix='/api')
    app.register_blueprint(bp_auth, url_prefix='/api')
    app.register_blueprint(like_api, url_prefix='/api')
    app.register_blueprint(comment_api, url_prefix='/api/comments')

    return app


@identity_loaded.connect_via(create_app)
def on_identity_loaded(sender, identity):
    identity.user = current_user

    if hasattr(current_user, 'username'):
        identity.provides.add(UserNeed(current_user.username))

    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.rolename))
