from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_mail import Message
from sqlalchemy import and_

from . import mail
from .forms import SubscribeForm
from .models import (Pincodes, Preference, SubscriberPincodePreferences,
                     Subscribers, db)

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

    mail.send(Message('Subscribied successfully for Cowin Alerts!',
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
            preference = Preference.find(
                sub_form.sub_18.data,
                sub_form.sub_45.data,
            )
            subscriber = Subscribers.get_or_create(
                sub_form.email.data.lower().strip(),
                sub_form.name.data.lower(),
            )

            subscription = SubscriberPincodePreferences.query.filter(and_(
                SubscriberPincodePreferences.subscriber == subscriber, SubscriberPincodePreferences.pincode == pincode)).first()

            if subscription:
                subscription.preference = preference
            else:
                subscription = SubscriberPincodePreferences(
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


@index_bp.get('/r')
def run():
    return render_template('vaccine-available.html')
