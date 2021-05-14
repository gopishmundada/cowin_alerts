from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class SubscribeForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[DataRequired()],
    )
    email = StringField(
        'Email',
        validators=[DataRequired()],
    )
    pincode = StringField(
        'Pincode',
        validators=[DataRequired()],
    )
    sub_18 = BooleanField('18+')
    sub_45 = BooleanField('45+')
    submit = SubmitField('Subscribe')
