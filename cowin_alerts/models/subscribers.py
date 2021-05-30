from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, UniqueConstraint

from ._db import db


class SubscriberPincodePreferences(db.Model):
    __tablename__ = 'subscriber_pincode_preferences'

    id = Column(Integer, primary_key=True)

    subscriber_id = Column(Integer, ForeignKey(
        "subscribers.id"), nullable=False)
    postal_index = Column(Integer, ForeignKey(
        "pincodes.pincode"), nullable=False)
    preference_id = Column(Integer, ForeignKey(
        "preference.id"), nullable=False)

    __table_args__ = (UniqueConstraint(
        subscriber_id,
        postal_index,
        preference_id),)

    subscriber = db.relationship(
        "Subscribers",
        back_populates="subscriptions",
    )
    preference = db.relationship('Preference')
    pincode = db.relationship(
        "Pincodes",
        back_populates="subscriptions",
    )


class Subscribers(db.Model):
    __tablename__ = 'subscribers'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(13), unique=True)

    subscriptions = db.relationship(
        'SubscriberPincodePreferences',
        back_populates="subscriber"
    )


class Pincodes(db.Model):
    __tablename__ = 'pincodes'

    pincode = Column(Integer, primary_key=True, autoincrement=False)
    sub_18_last_mail_sent_on = Column(DateTime)
    sub_45_last_mail_sent_on = Column(DateTime)

    subscriptions = db.relationship(
        'SubscriberPincodePreferences',
        back_populates="pincode"
    )


class Preference(db.Model):
    __tablename__ = 'preference'

    id = Column(Integer, primary_key=True)
    sub_18 = Column(Boolean, nullable=False)
    sub_45 = Column(Boolean, nullable=False)
