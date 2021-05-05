import datetime

from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property

from api2 import db, ma
from marshmallow import fields, validate, EXCLUDE
from api2.models.likes_table import likes


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    inserted_at = db.Column(db.DateTime, default=datetime.date.today())
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow())
    type = db.Column(db.String(255))
    priority = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    likes = db.relationship('User', secondary=likes, backref='post', lazy='dynamic')

    @hybrid_property
    def likes_quantity(self):
        post = Post.query.filter(Post.id == self.id).first_or_404()
        return post.likes.count()

    @hybrid_property
    def post_comments(self):
        post = Post.query.filter(Post.id == self.id).first_or_404()
        return post.comments.count()

    @hybrid_property
    def order_by_likes_quantity(self):
        return Post.query.outerjoin(likes).group_by(Post.id).order_by(db.func.count(likes.id).desc())

    def __repr__(self):
        return self.title


class PostSchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Integer(dump_only=True)
    title = fields.String(validate=validate.Length(max=255))
    description = fields.String(validate=validate.Length(max=500))
    inserted_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    type = fields.String(validate=validate.Length(max=255))
    priority = fields.Integer()
    user_id = fields.Integer(dump_only=True)
