from datetime import datetime, timedelta

import requests
from flask import current_app
from flask.templating import render_template
from flask_mail import Message
from requests.exceptions import HTTPError
from sqlalchemy import and_

from cowin_alerts.models.subscribers import Preference

from . import mail
from .models import Pincodes, Subscriptions, db
from .scheduler import scheduler

EMAIL_SUBJECT = 'Vaccine slots available for {}+'
EMAIL_BODY = 'Dear User, \nVaccine slots are available.\nAge group: {}+\n Available Slots: {}\nPincode: {}.\n Book your vaccine now!'


def get_todays_data(pincode: int) -> dict:
    api_url = current_app.config.get('CALENDER_BY_PIN_URL')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    }
    params = {
        'pincode': pincode,
        'date': datetime.now().strftime("%d-%m-%Y"),
    }

    res = requests.get(url=api_url, params=params, headers=headers)
    res.raise_for_status()

    return res.json()


def get_slots(json_data: dict) -> tuple:
    avail_data_45 = avail_data_18 = 0

    for x in range(len(json_data['centers'])):
        for y in range(len(json_data['centers'][x]['sessions'])):
            if json_data['centers'][x]['sessions'][y]['min_age_limit'] == 45:
                avail_data_45 += json_data['centers'][x]['sessions'][y]['available_capacity']
            else:
                avail_data_18 += json_data['centers'][x]['sessions'][y]['available_capacity']

    return avail_data_18, avail_data_45


def can_send_mail(slots: int, mail_sent_on: datetime) -> bool:
    if slots and slots > 0:
        if isinstance(mail_sent_on, datetime):
            last_hour = datetime.now() - timedelta(hours=current_app.config.get('ALERT_DELAY_HOURS',24))
            return mail_sent_on < last_hour
        else:
            return True

    return False


def send_available_email(
    recipients: list,
    last_mail_on: datetime,
    slots: int,
    subject: str,
    pincode: str,
) -> bool:
    '''
    Sends vaccine availability mail to recipients if mail can be send.
    Checks for number of available slots and last mail sent datetime.

    :param recipients: List of user name and email e.g [('John','john@wick.com'), ('Tony', 'tony@stark.com')]
    :return: True if mail sent successfully False otherwise.
    '''

    if len(recipients) == 0:
        return False
    if not can_send_mail(slots, last_mail_on):
        return False

    for name, email in recipients:
        body = render_template('vaccine-available.html',
                               name=name,
                               email=email,
                               slots=slots,
                               pincode=pincode)
        mail.send(Message(subject=subject, html=body, recipients=[email]))

    return True


def get_subscribers_list(district: Pincodes, sub_18: bool, sub_45: bool):
    '''
    Returns list of user name and email e.g [('John','john@wick.com'), ('Tony', 'tony@stark.com')]
    '''

    if sub_18 == None and sub_45 == None:
        raise ValueError('Both args cannot be None')

    if sub_18 != None and sub_45 != None:
        preference = Preference.get_or_create(sub_18, sub_45)
        condition = and_(Subscriptions.preference == preference,
                         Subscriptions.pincode == district)
        return list(map(lambda u: (u.subscriber.name, u.subscriber.email),
                               Subscriptions.query.filter(condition)))
    elif sub_18 != None:
        preferences = Preference.query.filter_by(sub_18=sub_18)
        recipients = []

        for pref in preferences:
            recipients += list(map(lambda u: (u.subscriber.name, u.subscriber.email),
                                   Subscriptions.query.filter_by(pincode_id=district.id,
                                                                 preference_id=pref.id)))

        return recipients
    else:
        preferences = Preference.query.filter_by(sub_45=sub_45)
        recipients = []

        for pref in preferences:
            condition = and_(Subscriptions.preference == pref,
                             Subscriptions.pincode == district)
            recipients += list(map(lambda u: (u.subscriber.name, u.subscriber.email),
                                   Subscriptions.query.filter_by(pincode_id=district.id,
                                                                 preference_id=pref.id)))

        return recipients


def check_slots_and_send_email(district: Pincodes) -> None:
    if not isinstance(district, Pincodes):
        raise ValueError('Required instance of <Pincodes>')

    slots_data = get_todays_data(district.pincode)
    slots_18, slots_45 = get_slots(slots_data)

    # Send mail to 18+ subscribers if slots are available
    status_18 = send_available_email(
        recipients=get_subscribers_list(district, True, None),
        last_mail_on=district.sub_18_last_mail_sent_on,
        slots=slots_18,
        subject=EMAIL_SUBJECT.format(18),
        pincode=district.pincode,
    )
    if status_18:  # Update last mail time
        district.sub_18_last_mail_sent_on = datetime.now()
        db.session.commit()
        print(f'** Mail sent: <{district.pincode} 18+>')

    # Send mail to 45+ subscribers if slots are available
    status_45 = send_available_email(
        recipients=get_subscribers_list(district, None, True),
        last_mail_on=district.sub_45_last_mail_sent_on,
        slots=slots_45,
        subject=EMAIL_SUBJECT.format(45),
        pincode=district.pincode,
    )
    if status_45:  # Update last mail time
        district.sub_45_last_mail_sent_on = datetime.now()
        db.session.commit()
        print(f'** Mail sent: <{district.pincode} 45+>')


@scheduler.task(
    "interval",
    id="check_all_pincodes",
    seconds=30,
    max_instances=1,
)
def scheduled_check_all_pincodes() -> None:
    with scheduler.app.app_context():
        print('** Checking for slots...')

        for district in Pincodes.query.all():
            try:
                check_slots_and_send_email(district)
            except ValueError as vErr:
                print(f'Value Error: {vErr}')
            except HTTPError as httpErr:
                print(f'Request Error: {httpErr}')
