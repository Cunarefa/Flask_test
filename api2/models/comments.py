import datetime

from marshmallow import fields, validate
from marshmallow import EXCLUDE

from api2 import db, ma


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500))
    inserted_at = db.Column(db.DateTime, default=datetime.date.today())
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))


class CommentSchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE

    content = fields.String(validate=validate.Length(max=255), required=True)
    inserted_at = fields.DateTime(dump_only=True)
    author_id = fields.Integer(dump_only=True)
    post_id = fields.Integer(dump_only=True)
