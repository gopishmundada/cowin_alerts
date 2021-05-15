from apscheduler.schedulers.background import BackgroundScheduler
from flask import Blueprint, flash, render_template, request, url_for
from werkzeug.utils import redirect

from .forms import SubscribeForm
from .models import Subscribers, db
from .utils import scheduled_job

scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(scheduled_job, 'interval', seconds=10)
scheduler.start()


index_bp = Blueprint(
    'index_bp',
    __name__,
    template_folder='templates',
    static_folder='static'
)


@index_bp.route('/', methods=['GET', 'POST'])
def index():
    sub_form = SubscribeForm()
    success = request.args.get('success') or False

    if sub_form.validate_on_submit():
        if not sub_form.sub_18.data and not sub_form.sub_45.data:
            flash('Please select at least 1 age group')
        else:
            subscriber = Subscribers(
                name=sub_form.name.data.strip(),
                email=sub_form.email.data,
                pincode=sub_form.pincode.data,
                sub_18=sub_form.sub_18.data,
                sub_45=sub_form.sub_45.data,
            )

            db.session.add(subscriber)
            db.session.commit()

            return redirect(url_for('index_bp.index', success=True))

    return render_template(
        'index.html',
        title='Cowin Alerts',
        sub_form=sub_form,
        success=success,
    )
