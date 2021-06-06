def test_getIndexPage(client):
    response = client.get('/')

    assert response.status_code == 200
    assert 'India Cowin Alerts' in response.get_data(as_text=True)


def test_SubscribeNewUserNewPincode(client):
    data = dict(
        name='John Wick',
        email='john@wick.com',
        pincode=431203,
        sub_18=True,
        sub_45=False,
        submit=True
    )

    response = client.post('/', data=data, follow_redirects=True)

    assert response.status_code == 200
    assert 'You have successfully registered for' in response.get_data(
        as_text=True)


def test_SubscribeNewUserInvalidPincode(client):
    data = dict(
        name='John Wick',
        email='john@wick.com',
        pincode=432103,  # Invalid Pincode
        sub_18=True,
        sub_45=False,
        submit=True
    )

    response = client.post('/', data=data, follow_redirects=True)

    assert response.status_code == 200
    assert 'Pincode does not exists' in response.get_data(as_text=True)


def test_SubscribeNewUserNewPincodeNoAgeGroup(client):
    data = dict(
        name='John Wick',
        email='john@wick.com',
        pincode=431203,
        submit=True
    )

    response = client.post('/', data=data, follow_redirects=True)

    assert response.status_code == 200
    assert 'Please select at least 1 age group' in response.get_data(
        as_text=True)


def test_SubscribeExistingUserNewPincode(client):
    data = dict(
        name='John Wick',
        email='john@wick.com',
        pincode=431203,
        sub_18=True,
        sub_45=False,
        submit=True
    )

    # Subscribing for first pincode
    response = client.post('/', data=data, follow_redirects=True)
    assert response.status_code == 200

    # Subscribing for second pincode
    data['pincode'] = 431204
    response = client.post('/', data=data, follow_redirects=True)

    assert response.status_code == 200
    assert 'You have successfully registered for' in response.get_data(
        as_text=True)


def test_SubscribeNewUserExistingPincode(client):
    data = dict(
        name='First User',
        email='first@gmail.com',
        pincode=431203,
        sub_18=True,
        sub_45=False,
        submit=True
    )

    # First user new pincode
    response = client.post('/', data=data, follow_redirects=True)
    assert response.status_code == 200

    # Second user existing pincode
    data['email'] = 'Second User'
    data['email'] = 'second@gmail.com'
    response = client.post('/', data=data, follow_redirects=True)

    assert response.status_code == 200
    assert 'You have successfully registered for' in response.get_data(
        as_text=True)


def test_SubscribeExisitingUserExistingPincodeUpdatePreference(client):
    data = dict(
        name='First User',
        email='first@gmail.com',
        pincode=431203,
        sub_18=False,
        sub_45=True,
        submit=True
    )

    # First user new pincode
    response = client.post('/', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert 'You have successfully registered for' in response.get_data(
        as_text=True)

    # Existing user existing pincode updated preferences
    data['sub_18'] = True
    data['sub_45'] = False
    response = client.post('/', data=data, follow_redirects=True)

    assert response.status_code == 200
    assert 'Your preferences have been updated' in response.get_data(
        as_text=True)
