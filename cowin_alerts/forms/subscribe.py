from flask_wtf import FlaskForm
from requests import get
from requests.api import request
from wtforms import BooleanField, IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
from wtforms.widgets.html5 import NumberInput


class PincodeValidator(object):
    POSTAL_CODE_API = 'https://api.postalpincode.in/pincode/{}'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    }

    def __init__(self, message='Invalid Pincode'):
        self.message = message

    def __call__(self, form, field):
        if not field.data:
            raise ValidationError(self.message)

        response = get(
            url=self.POSTAL_CODE_API.format(field.data),
            headers=self.HEADERS
        )

        if response.status_code != 200 or response.json()[0]['Status'] != 'Success':
            raise ValidationError('Pincode does not exists')


class SubscribeForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[DataRequired()],
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message='Enter a valid email.'),
        ],
    )
    pincode = IntegerField(
        'Pincode',
        validators=[
            DataRequired(),
            PincodeValidator(),
        ],
        widget=NumberInput(),
    )
    sub_18 = BooleanField('18+')
    sub_45 = BooleanField('45+')
    submit = SubmitField('Subscribe')
