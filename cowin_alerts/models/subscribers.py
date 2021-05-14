from ._db import db


class Subscribers(db.Model):
    __tablename__ = 'subscribers'
    id = db.Column(
        'id',
        db.Integer,
        primary_key=True,
    )
    first_name = db.Column(
        'first_name',
        db.String(64),
        nullable=False,
    )
    last_name = db.Column(
        'last_name',
        db.String(64),
        nullable=False,
    )
    email = db.Column(
        'email',
        db.String(512),
        nullable=False,
    )
    pincode = db.Column(
        'pincode',
        db.String(6),
        nullable=False,
    )
    sub_18 = db.Column(
        'sub_18',
        db.Boolean,
        nullable=False,
    )
    sub_45 = db.Column(
        'sub_45',
        db.Boolean,
        nullable=False,
    )
