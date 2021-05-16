from flask import Blueprint, flash, render_template, request, url_for
from flask_mail import Message
from werkzeug.utils import redirect

from . import mail
from .forms import SubscribeForm
from .models import Subscribers, db
from .utils import scheduler

index_bp = Blueprint(
    'index_bp',
    __name__,
    template_folder='templates',
    static_folder='static'
)

scheduler.start()


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

            msg = Message('Subscribied successfully for Cowin Alerts!',
                          recipients=[sub_form.email.data.strip()], html='<b>Testing</b> asdkcnoi')

            mail.send(msg)

            return redirect(url_for('index_bp.index', success=True))

    return render_template(
        'index.html',
        title='Cowin Alerts',
        sub_form=sub_form,
        success=success,
    )
