from datetime import datetime, timedelta
from os import environ

import requests
from flask_mail import Message
from flask import current_app
from requests.models import HTTPError

from . import mail
from .models import Pincodes, db
from .scheduler import scheduler


def fetch_todays_data(pincode):
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


def get_slots(json_data):
    avail_data_45 = avail_data_18 = 0

    for x in range(len(json_data['centers'])):
        for y in range(len(json_data['centers'][x]['sessions'])):
            if json_data['centers'][x]['sessions'][y]['min_age_limit'] == 45:
                avail_data_45 += json_data['centers'][x]['sessions'][y]['available_capacity']
            else:
                avail_data_18 += json_data['centers'][x]['sessions'][y]['available_capacity']

    return avail_data_18, avail_data_45


def send_available_email(subject='Vaccine slots available!', body='Email body', recipients=None):
    if not isinstance(recipients, list):
        raise ValueError('Empty recipients list.')
    if len(recipients) == 0:
        raise ValueError('Empty recipients list.')

    msg = Message(
        subject=subject,
        html=body,
        recipients=recipients
    )
    mail.send(msg)


def can_send_mail(slots: int, mail_sent_on: datetime) -> bool:
    if slots and slots > 0:
        if isinstance(mail_sent_on, datetime):
            last_hour = datetime.now() - timedelta(hours=1)
            return mail_sent_on < last_hour
        else:
            return True

    return False


def check_and_send_email(pincode: Pincodes):
    if not isinstance(pincode, Pincodes):
        raise ValueError(
            'check_ans_send_email() requires instance of <Pincodes>')

    slots_data = fetch_todays_data(pincode.pincode)

    slots_18, slots_45 = get_slots(slots_data)

    if can_send_mail(slots_18, pincode.sub_18_last_mail_sent_on):
        try:
            send_available_email(
                subject='Vaccine slots available for 18+',
                body='Dear User, \nVaccine slots are available.\nAge group: 18+\n Available Slots: {}\nPincode: {}.\n Book your vaccine now!'.format(
                    slots_18, pincode.pincode),
                recipients=[
                    sub.email for sub in pincode.subscribers if sub.sub_18 == True]
            )
            pincode.sub_18_last_mail_sent_on = datetime.now()

            print(f'===> Mail sent: <{pincode.pincode}>')
            db.session.commit()
        except ValueError as e:
            print(f'===> ERROR: {e}')

    if can_send_mail(slots_45, pincode.sub_45_last_mail_sent_on):
        try:
            send_available_email(
                subject='Vaccine slots available for 45+',
                body='Dear User, \nVaccine slots are available.\nAge group: 45+\n Available Slots: {}\nPincode: {}.\n Book your vaccine now!'.format(
                    slots_18, pincode.pincode),
                recipients=[
                    sub.email for sub in pincode.subscribers if sub.sub_45 == True]
            )
            pincode.sub_45_last_mail_sent_on = datetime.now()

            print(f'===> Mail sent: <{pincode.pincode}>')
            db.session.commit()
        except ValueError as e:
            print(f'===> ERROR: {e}')


@scheduler.task(
    "interval",
    id="check_all_pincodes",
    seconds=30,
    max_instances=1,
)
def scheduled_check_all_pincodes():
    with scheduler.app.app_context():
        print('==> Checking for slots...')

        for district in Pincodes.query.all():
            try:
                check_and_send_email(district)
            except ValueError as vErr:
                print(f'==> ERROR: {vErr} <==')
            except HTTPError as httpErr:
                print(f'==> ERROR: {httpErr} <==')
