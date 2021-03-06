from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_mail import Message
from sqlalchemy import and_

from . import mail
from .forms import SubscribeForm
from .models import Pincodes, Preference, Subscriptions, Users, db

index_bp = Blueprint(
    'index_bp',
    __name__,
    template_folder='templates',
    static_folder='static'
)


def send_subscriber_success_mail(email: str, pincode: int, user_name: str = 'User') -> None:
    '''
    Sends a subscribe success email to the provided email

        :param email: E-mail address of the user
        :param pincode: Pincode for which the user has subscribed
        :param user_name: Name of the user
    '''
    success_msg = render_template(
        'subscribe-success-mail.html',
        user_name=user_name,
        pincode=pincode,
    )

    mail.send(Message('Subscribed successfully for Cowin Alerts!',
                      recipients=[email],
                      html=success_msg))


@index_bp.route('/', methods=['GET', 'POST'])
def index():
    sub_form = SubscribeForm()
    form_status = request.args.get('success')

    if sub_form.validate_on_submit():
        if not sub_form.sub_18.data and not sub_form.sub_45.data:
            flash('Please select at least 1 age group')
        else:
            pincode = Pincodes.get_or_create(sub_form.pincode.data)
            preference = Preference.get_or_create(
                sub_form.sub_18.data,
                sub_form.sub_45.data,
            )
            subscriber = Users.get_or_create(
                sub_form.email.data.lower().strip(),
                sub_form.name.data.strip(),
            )

            subscription = Subscriptions.query.filter(and_(
                Subscriptions.subscriber == subscriber, Subscriptions.pincode == pincode)).first()

            if subscription:
                subscription.preference = preference
            else:
                subscription = Subscriptions(
                    subscriber=subscriber,
                    pincode=pincode,
                    preference=preference,
                )
                db.session.add(subscription)

            db.session.commit()

            send_subscriber_success_mail(
                email=subscriber.email,
                pincode=pincode.pincode,
                user_name=subscriber.name
            )

            return redirect(url_for('index_bp.index', success=True))

    return render_template(
        'index.html',
        title='Cowin Alerts',
        sub_form=sub_form,
        success=form_status,
    )


@index_bp.post('/unsubscribe/<string:email>')
def unsubscribe(email):
    user = Users.query.filter(Users.email == email).first()

    if not user:
        return 'User not found', 400

    Subscriptions.query.filter(
        Subscriptions.subscriber == user).delete()
    db.session.commit()

    return 'Successfully unsubscribed'


@index_bp.get('/run')
def run():
    return render_template('vaccine-available.html', name='Akshay', email='aksahy@gmail.com', slots=123, pincode=32341)
