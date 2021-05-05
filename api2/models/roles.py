from api2 import db


class Role(db.Model):
    __tablename__ = 'roles'

    rolename = db.Column(db.String(60), primary_key=True)
    username = db.Column(db.String(100), db.ForeignKey('users.username'))
