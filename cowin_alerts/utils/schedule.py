import smtplib
from datetime import datetime, timedelta

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app
from flask_mail import Message

from .. import mail
from ..models import Pincodes, db

s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login(current_app.config.get('MAIL_USERNAME'),
        current_app.config.get('MAIL_PASSWORD'))


def fetch_todays_data(pincode):
    api_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    }
    params = {
        'pincode': pincode,
        'date': datetime.now().strftime("%d-%m-%Y"),
    }

    res = requests.get(url=api_url, params=params, headers=headers)

    if res.status_code == 200:
        return res
    else:
        return None


def get_slots(jsonData, i):
    avail_data_45 = avail_data_18 = 0

    for x in range(len(jsonData['centers'])):
        for y in range(len(jsonData['centers'][x]['sessions'])):
            if jsonData['centers'][x]['sessions'][y]['min_age_limit'] == 45:
                avail_data_45 += jsonData['centers'][x]['sessions'][y]['available_capacity']
            else:
                avail_data_18 += jsonData['centers'][x]['sessions'][y]['available_capacity']

    return avail_data_18, avail_data_45


def send_available_email(subject='Vaccine slots available!', body='Email body', recipients=None):
    if recipients == None:
        raise ValueError('Empty recipients list.')

    msg = Message(
        subject=subject,
        html=body,
        recipients=recipients
    )
    mail.send(msg)


def scheduled_job():
    pass


def check_and_send_email_scheduled():
    pincode = Pincodes.query.get(431203)

    response = fetch_todays_data(pincode.pincode)

    if response == None:
        return

    slots_18, slots_45 = get_slots(response.json())

    last_hour = datetime.now() - timedelta(hours=1)

    should_send_18 = pincode.sub_18_last_mail_sent_on < last_hour
    should_send_45 = pincode.sub_45_last_mail_sent_on < last_hour

    if slots_18 > 0 and should_send_18:
        send_available_email(
            subject='Vaccine slots available for 18+',
            body=f'Dear User, \nVaccine slots are available.\nAge group: 18+\n Available Slots: {slots_18}\nPincode: {pincode.pincode}.\n Book your vaccine now!',
            recipients=[sub.email for sub in pincode.subscribers if sub.sub_18]
        )

    if slots_45 > 0 and should_send_45:
        send_available_email(
            subject='Vaccine slots available for 45+',
            body=f'Dear User, \n Vaccine slots are available.\nAge group: 45+\n Available Slots: {slots_45}\nPincode: {pincode.pincode}.\n Book your vaccine now!',
            recipients=[sub.email for sub in pincode.subscribers if sub.sub_18]
        )


scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(scheduled_job, 'interval',
                  seconds=current_app.config.get('ALERT_INTERVAL'))
