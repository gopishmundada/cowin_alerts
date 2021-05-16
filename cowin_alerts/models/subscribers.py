from ._db import db


subscriber_pincode = db.Table(
    'subscriber_pincode',
    db.Column(
        'subscriber_id',
        db.Integer,
        db.ForeignKey('subscribers.id'),
        primary_key=True,
    ),
    db.Column(
        'pincode',
        db.Integer,
        db.ForeignKey('pincodes.pincode'),
        primary_key=True,
    ),
)


class Subscribers(db.Model):
    __tablename__ = 'subscribers'
    id = db.Column(
        'id',
        db.Integer,
        primary_key=True,
    )
    name = db.Column(
        'name',
        db.String(64),
        nullable=False,
    )
    email = db.Column(
        'email',
        db.String(512),
        nullable=False,
    )
    phone = db.Column(
        'phone',
        db.String(13),
        nullable=True,
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
    pincodes = db.relationship(
        'Pincodes',
        secondary=subscriber_pincode,
        backref=db.backref(
            'subscribers',
            lazy='dynamic',
        )
    )


class Pincodes(db.Model):
    __tablename__ = 'pincodes'
    pincode = db.Column(
        'pincode',
        db.Integer,
        primary_key=True,
    )
    last_mail_sent_on = db.Column(
        'last_mail_sent',
        db.DateTime,
        nullable=True,
    )
    subscribers = db.relationship(
        'Subscribers',
        secondary=subscriber_pincode,
        backref=db.backref(
            'pincodes',
            lazy='dynamic',
        )
    )
