from os import name
from cowin_alerts.forms import SubscribeForm


def test_getIndexPage(app):
    with app.test_client() as client:
        response = client.get('/')

        assert response.status_code == 200
        assert 'India Cowin Alerts' in response.get_data(as_text=True)


def test_SubscribeNewUserNewPincode(app):
    with app.test_client() as client:
        data = dict(
            name='John Wick',
            email='john@wick.com',
            pincode=431203,
            sub_18=True,
            sub_45=True,
            submit=True
        )

        form = SubscribeForm(
            name='Akshay', email='shegaoka@gmail.com', pincode=431203, sub_18=True, sub_45=True, submit=True)

        response = client.post('/', data=form.data, follow_redirects=True)

        print(response.get_data(
            as_text=True))

        assert response.status_code == 200
        assert 'You have successfully registered for' in response.get_data(
            as_text=True)
