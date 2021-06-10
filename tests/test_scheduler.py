from cowin_alerts.check_slots import get_subscribers_list
from cowin_alerts.models import (Pincodes, Preference,
                                 Subscriptions, Users, db)


def test_getRecipientsList(app):
    district1 = Pincodes(pincode=431203)
    district2 = Pincodes(pincode=431204)
    user1 = Users(email='tony@stark.com', name='Ironman')

    db.session.add_all([district1, district2, user1])
    db.session.commit()

    subscriptions = [
        Subscriptions(
            subscriber=user1,
            pincode=district1,
            preference=Preference.get_or_create(True, True),
        ),
        Subscriptions(
            subscriber=Users(email='arya@stark.com', name='Needle'),
            pincode=district1,
            preference=Preference.get_or_create(True, False),
        ),
        Subscriptions(
            subscriber=user1,
            pincode=district2,
            preference=Preference.get_or_create(True, True),
        ),
        Subscriptions(
            subscriber=Users(email='maha@dev.com', name='Bhole'),
            pincode=district1,
            preference=Preference.get_or_create(True, True),
        ),
    ]

    db.session.add_all(subscriptions)
    db.session.commit()

    jalna = Pincodes.query.filter(Pincodes.pincode == 431203).first()

    # Strict conditions
    assert [
        ('Ironman', 'tony@stark.com'),
        ('Bhole', 'maha@dev.com'),
    ] == get_subscribers_list(jalna, True, True)
    assert [('Needle', 'arya@stark.com')
            ] == get_subscribers_list(jalna, True, False)
    assert [] == get_subscribers_list(jalna, False, True)

    # Non strict conditions
    assert [
        ('Ironman', 'tony@stark.com'),
        ('Bhole', 'maha@dev.com'),
        ('Needle', 'arya@stark.com'),
    ] == get_subscribers_list(jalna, True, None)
    assert [
        ('Ironman', 'tony@stark.com'),
        ('Bhole', 'maha@dev.com'),
    ] == get_subscribers_list(jalna, None, True)
