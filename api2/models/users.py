from marshmallow import fields, validate, EXCLUDE
from werkzeug.security import generate_password_hash, check_password_hash

from api2 import db, ma


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(128))

    def __repr__(self):
        return f'User - {self.username}'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        unknown = EXCLUDE

    username = fields.String(validate=validate.Length(min=3), required=True)
    password = fields.String(required=True, validate=validate.Length(min=6, max=36), load_only=True)
    email = fields.Email(required=True, validate=validate.Length(100))
