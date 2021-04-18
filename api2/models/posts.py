import datetime

from api2 import db, ma
from marshmallow import fields, validate, EXCLUDE


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    inserted_at = db.Column(db.Date, default=datetime.date.today())
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow())
    type = db.Column(db.String(255))
    priority = db.Column(db.Integer)

    def __repr__(self):
        return self.title


class PostSchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(dump_only=True)
    title = fields.String(validate=validate.Length(max=255), required=True)
    description = fields.String(validate=validate.Length(max=500))
    inserted_at = fields.Date(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    type = fields.String(validate=validate.Length(max=255))
    priority = fields.Integer()
