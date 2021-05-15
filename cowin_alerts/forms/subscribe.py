from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email, ValidationError


class Pincode(object):
    def __init__(self, message='Invalid Pincode'):
        self.message = message

    def __call__(self, form, field):
        if field.data is None:
            raise ValidationError(self.message)
        data = str(field.data)
        if len(data) != 6 and data.isnumeric():
            raise ValidationError(self.message)

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
            Pincode(),
        ],
    )
    sub_18 = BooleanField('18+')
    sub_45 = BooleanField('45+')
    submit = SubmitField('Subscribe')
