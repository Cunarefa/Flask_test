from marshmallow import fields, validate
from werkzeug.security import generate_password_hash, check_password_hash

from api2 import db, ma


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f'User - {self.username}'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

    username = fields.String(validate=validate.Length(min=3), required=True)
    email = fields.Email(required=True, validate=validate.Length(100))
