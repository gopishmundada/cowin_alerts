from cowin_alerts.models import Users, Pincodes, Preference, Subscriptions


def test_tableNames(vaccine_db):
    assert vaccine_db.users_table == Users.__tablename__
    assert vaccine_db.pincodes_table == Pincodes.__tablename__
    assert vaccine_db.preference_table == Preference.__tablename__
    assert vaccine_db.subscriptions_table == Subscriptions.__tablename__


def test_getAllPincodes(vaccine_db):
    pincodes = vaccine_db.get_all_pincodes()

    assert pincodes == [431203, 431204, 410507]


def test_getSubscribersList(vaccine_db):
    assert vaccine_db.get_subscribers_list(
        pincode=431203,
        sub_18=True,
        sub_45=True,
    ) == [('John Wick', 'john@wick.com'), ('Tony Stark', 'tony@stark.com')]

    assert vaccine_db.get_subscribers_list(
        pincode=410507,
        sub_18=True,
        sub_45=True,
    ) == [('Tony Stark', 'tony@stark.com')]

    assert vaccine_db.get_subscribers_list(
        pincode=410507,
        sub_18=True,
        sub_45=False,
    ) == [('Needle', 'arya@stark.com')]

    assert vaccine_db.get_subscribers_list(
        pincode=431204,
        sub_18=False,
        sub_45=True,
    ) == [('John Wick', 'john@wick.com')]

    assert vaccine_db.get_subscribers_list(
        pincode=431203,
        sub_18=True,
        sub_45=False,
    ) == []

    assert vaccine_db.get_subscribers_list(
        pincode=431203,
        sub_18=True,
        sub_45=None,
    ) == [('John Wick', 'john@wick.com'), ('Tony Stark', 'tony@stark.com')]

    assert vaccine_db.get_subscribers_list(
        pincode=431203,
        sub_18=None,
        sub_45=True,
    ) == [('John Wick', 'john@wick.com'), ('Needle', 'arya@stark.com'), ('Tony Stark', 'tony@stark.com')]
