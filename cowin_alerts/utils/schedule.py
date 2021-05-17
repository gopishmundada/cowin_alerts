from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app
from ..models import Pincodes, db
from datetime import datetime


def scheduled_job():
    print(f'======> Job run:')


scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(scheduled_job, 'interval',
                  seconds=current_app.config.get('ALERT_INTERVAL'))


def test_date():
    pincode = Pincodes.query.get(431203)

    pincode.last_mail_sent_on = datetime.now()

    db.session.commit()
