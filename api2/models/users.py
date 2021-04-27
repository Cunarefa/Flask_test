import datetime
from flask_jwt_extended import create_access_token
from marshmallow import fields, validate, EXCLUDE
from api2 import db, ma
from api2.models.enums import Role, Sex
from marshmallow_enum import EnumField

from sqlalchemy.ext.hybrid import hybrid_property


DATE_FORMAT = '%d-%m-%Y'

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    date_of_birth = db.Column(db.Date)
    country = db.Column(db.String(100))
    role = db.Column(db.Enum(Role))
    sex = db.Column(db.Enum(Sex))
    age = db.Column('user_age', db.Integer)

    def __repr__(self):
        return f'User - {self.username}'

    def create_jwt_token(self):
        token = create_access_token(
            identity=self.username, expires_delta=datetime.timedelta(days=1))
        return token

    @hybrid_property
    def user_age(self):
        age = (datetime.date.today() - self.date_of_birth).days // 365
        return age


class UserRegisterSchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(dump_only=True)
    username = fields.String(required=True, validate=validate.Length(min=3))
    email = fields.Email(required=True, validate=validate.Length(max=100))
    password = fields.String(required=True, validate=validate.Length(max=128), load_only=True)
    date_of_birth = fields.Date(format=DATE_FORMAT)
    country = fields.String(validate=validate.Length(max=100))
    role = EnumField(Role, allow_none=True, by_value=True)
    sex = EnumField(Sex, allow_none=True, by_value=True)


class UserLoginSchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(dump_only=True)
    username = fields.String(required=True, validate=validate.Length(min=3))
    password = fields.String(required=True, validate=validate.Length(max=128), load_only=True)
    email = fields.Email(validate=validate.Length(max=100))
