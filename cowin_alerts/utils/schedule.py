from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app


def scheduled_job():
    print(f'======> Job run:')


scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(scheduled_job, 'interval',
                  seconds=current_app.config.get('ALERT_INTERVAL'))
