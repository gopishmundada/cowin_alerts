from flask import Blueprint, render_template
from .forms import SubscribeForm
from .models import Subscribers, db
from apscheduler.schedulers.background import BackgroundScheduler


def scheduled_job():
    print(f'======> Job run:')


sched = BackgroundScheduler(daemon=True)
sched.add_job(scheduled_job, 'interval', seconds=10)
sched.start()


index_bp = Blueprint(
    'index_bp',
    __name__,
    template_folder='templates',
    static_folder='static'
)


@index_bp.route('/', methods=['GET', 'POST'])
def index():
    sub_form = SubscribeForm()

    if sub_form.validate_on_submit():
        subscriber = Subscribers(
            name=sub_form.name.data,
            email=sub_form.email.data,
            pincode=sub_form.pincode.data,
            sub_18=sub_form.sub_18.data,
            sub_45=sub_form.sub_45.data,
        )

        db.session.add(subscriber)
        db.session.commit()

        return render_template(
            'success.html',
        )

    return render_template(
        'index.html',
        title='Cowin Alerts',
        sub_form=sub_form
    )
