from datetime import datetime, timedelta
from os import environ

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app
from flask_mail import Message

from .. import mail
from ..models import Pincodes, db

COWIN_API_TEST = 'https://api.demo.co-vin.in/api'
COWIN_API_PROD = 'https://cdn-api.co-vin.in/api'
CALENDER_BY_PIN_PATH = '/v2/appointment/sessions/public/calendarByPin'

CALENDER_BY_PIN_URL = ''
if environ.get('FLASK_ENV', 'Null') == 'production':
    CALENDER_BY_PIN_URL = COWIN_API_PROD + CALENDER_BY_PIN_PATH
else:
    CALENDER_BY_PIN_URL = COWIN_API_TEST + CALENDER_BY_PIN_PATH


def fetch_todays_data(pincode):
    api_url = CALENDER_BY_PIN_URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    }
    params = {
        'pincode': pincode,
        'date': datetime.now().strftime("%d-%m-%Y"),
    }

    res = requests.get(url=api_url, params=params, headers=headers)

    if res.status_code == 200:
        return res.json()
    else:
        return None


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
        return

    slots_data = fetch_todays_data(pincode.pincode)

    if not slots_data:
        return

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

            db.session.commit()
        except ValueError as e:
            print(f'===> ERROR: {str(e)}')

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

            db.session.commit()
        except ValueError as e:
            print(f'===> ERROR: {str(e)}')


def scheduled_check_all_pincodes():
    print('===> Checking for slots...')
    for district in Pincodes.query.all():
        check_and_send_email(district)


scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(scheduled_check_all_pincodes, 'interval',
                  seconds=current_app.config.get('ALERT_INTERVAL'))
