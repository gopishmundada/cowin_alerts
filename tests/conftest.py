import pytest
from cowin_alerts import create_app, db
from cowin_alerts.VaccineNotifier import VaccineNotifier
from cowin_alerts.VaccineDB import VaccineDB


@pytest.fixture
def app():
    app = create_app('testing')

    with app.app_context():
        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture
def notifier(vaccine_db):
    return VaccineNotifier(vaccine_db)


@pytest.fixture
def vaccine_db():
    vaccine_db = VaccineDB(testing=True)

    vaccine_db.populate_test_db()

    yield vaccine_db

    vaccine_db.drop_all()
