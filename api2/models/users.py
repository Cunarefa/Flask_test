import datetime

from flask_jwt_extended import create_access_token
from marshmallow import fields, validate, EXCLUDE
from werkzeug.security import generate_password_hash, check_password_hash

from api2 import db, ma


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'User - {self.username}'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def create_jwt_token(self):
        token = create_access_token(
            identity=self.username, expires_delta=datetime.timedelta(days=1))
        return token


class UserSchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(dump_only=True)
    username = fields.String(validate=validate.Length(min=3))
    email = fields.Email(required=True, validate=validate.Length(100))
    password = fields.String(validate=validate.Length(128), load_only=True)
