from cowin_alerts.models import Users, db


def test_getOrCreateModel(app):
    db.session.add(Users(email='john@wick.com', name='John Wick'))
    db.session.commit()

    john = Users.get_or_create(email='john@wick.com', name='John Wick')
    assert john.email == 'john@wick.com'

    new_user = Users.get_or_create(email='new@user.com', name='Newbie')

    newbie = Users.query.filter_by(email='new@user.com').first()
    assert newbie.email == 'new@user.com'
