from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, UniqueConstraint

from ._db import db


class SubscriberPincodePreferences(db.Model):
    __tablename__ = 'subscriber_pincode_preferences'

    id = Column(Integer, primary_key=True)

    subscriber_id = Column(Integer, ForeignKey(
        "subscribers.id"), nullable=False)
    pincode_id = Column(Integer, ForeignKey(
        "pincodes.id"), nullable=False)
    preference_id = Column(Integer, ForeignKey(
        "preference.id"), nullable=False)

    __table_args__ = (UniqueConstraint(
        subscriber_id,
        pincode_id,
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
    subscribed = Column(Boolean, nullable=False, default=True)

    subscriptions = db.relationship(
        'SubscriberPincodePreferences',
        back_populates="subscriber"
    )

    @classmethod
    def get_or_create(cls, email, name):
        subscriber = cls.query.filter_by(email=email).first()

        if not subscriber:
            subscriber = Subscribers(email=email, name=name)

            db.session.add(subscriber)
            db.session.commit()

        return subscriber


class Pincodes(db.Model):
    __tablename__ = 'pincodes'

    id = Column(Integer, primary_key=True)
    pincode = Column(Integer, nullable=False, unique=True)
    sub_18_last_mail_sent_on = Column(DateTime)
    sub_45_last_mail_sent_on = Column(DateTime)

    subscriptions = db.relationship(
        'SubscriberPincodePreferences',
        back_populates="pincode"
    )

    @classmethod
    def get_or_create(cls, pincode):
        district = Pincodes.query.filter(Pincodes.pincode == pincode).first()

        if not district:
            district = Pincodes(pincode=pincode)

            db.session.add(district)
            db.session.commit()

        return district


class Preference(db.Model):
    __tablename__ = 'preference'

    id = Column(Integer, primary_key=True)
    sub_18 = Column(Boolean, nullable=False)
    sub_45 = Column(Boolean, nullable=False)

    @classmethod
    def get_or_create(self, sub_18, sub_45):
        preference = Preference.query.filter_by(
            sub_18=sub_18, sub_45=sub_45).first()

        if not preference:
            preference = Preference(sub_18=sub_18, sub_45=sub_45)

            db.session.add(preference)
            db.session.commit()

        return preference
