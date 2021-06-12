from datetime import datetime, timedelta
import requests
from os import environ

DELAY = environ.get('ALERT_DELAY_HOURS', 24)


class VaccineNotifier:
    HOURS_DELAY = DELAY
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
                Chrome/90.0.4430.93 Safari/537.36',
    }

    def __init__(self):
        self.api_url_prod = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin'
        self.api_url_test = 'https://cdndemo-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin'

    def get_todays_data(self, pincode):
        params = {
            'pincode': pincode,
            'date': datetime.now().strftime("%d-%m-%Y"),
        }

        res = requests.get(
            url=self.api_url_prod,
            params=params,
            headers=self.HEADERS,
        )
        res.raise_for_status()

        return res.json()

    def get_number_of_slots(self, json_data: dict) -> tuple:
        avail_data_45 = avail_data_18 = 0

        for x in range(len(json_data['centers'])):
            for y in range(len(json_data['centers'][x]['sessions'])):
                if json_data['centers'][x]['sessions'][y]['min_age_limit'] == 45:
                    avail_data_45 += json_data['centers'][x]['sessions'][y]['available_capacity']
                else:
                    avail_data_18 += json_data['centers'][x]['sessions'][y]['available_capacity']

        return avail_data_18, avail_data_45

    def can_send_email(self, slots: int, mail_sent_on: datetime = None) -> bool:
        if slots and slots > 0:
            if isinstance(mail_sent_on, datetime):
                delay = datetime.now() - timedelta(hours=self.HOURS_DELAY)
                return mail_sent_on < delay
            else:
                return True

        return False

    def send_available_email(
        self,
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
        if not self.can_send_mail(slots, last_mail_on):
            return False

        for name, email in recipients:
            body = render_template('vaccine-available.html',
                                   name=name,
                                   email=email,
                                   slots=slots,
                                   pincode=pincode)
            mail.send(Message(subject=subject, html=body, recipients=[email]))

        return True
