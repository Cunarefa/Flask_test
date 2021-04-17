from api2 import db, ma
from marshmallow import fields, validate, EXCLUDE


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return self.title


class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        unknown = EXCLUDE

    id = fields.Integer(dump_only=True)
    title = fields.String(validate=validate.Length(max=255), required=True)
    description = fields.String(validate=validate.Length(max=500))

