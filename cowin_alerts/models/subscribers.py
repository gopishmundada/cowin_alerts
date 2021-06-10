from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, UniqueConstraint

from ._db import db


class Subscriptions(db.Model):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True)

    subscriber_id = Column(Integer, ForeignKey(
        "users.id"), nullable=False)
    pincode_id = Column(Integer, ForeignKey(
        "pincodes.id"), nullable=False)
    preference_id = Column(Integer, ForeignKey(
        "preference.id"), nullable=False)

    __table_args__ = (UniqueConstraint(
        subscriber_id,
        pincode_id,
        preference_id),)

    subscriber = db.relationship(
        "Users",
        back_populates="subscriptions",
    )
    preference = db.relationship(
        'Preference',
        back_populates='subscriptions',
    )
    pincode = db.relationship(
        "Pincodes",
        back_populates="subscriptions",
    )


class Users(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(13), unique=True)

    subscriptions = db.relationship(
        'Subscriptions',
        back_populates="subscriber"
    )

    @classmethod
    def get_or_create(cls, email, name):
        user = cls.query.filter_by(email=email).first()

        if not user:
            user = cls(email=email, name=name)

            db.session.add(user)
            db.session.commit()

        return user


class Pincodes(db.Model):
    __tablename__ = 'pincodes'

    id = Column(Integer, primary_key=True)
    pincode = Column(Integer, nullable=False, unique=True)
    sub_18_last_mail_sent_on = Column(DateTime)
    sub_45_last_mail_sent_on = Column(DateTime)

    subscriptions = db.relationship(
        'Subscriptions',
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

    subscriptions = db.relationship(
        'Subscriptions',
        back_populates="preference"
    )

    @classmethod
    def get_or_create(self, sub_18, sub_45):
        preference = Preference.query.filter_by(
            sub_18=sub_18, sub_45=sub_45).first()

        if not preference:
            preference = Preference(sub_18=sub_18, sub_45=sub_45)

            db.session.add(preference)
            db.session.commit()

        return preference
