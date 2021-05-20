from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_mail import Message

from cowin_alerts.models.subscribers import Pincodes

from . import mail
from .forms import SubscribeForm
from .models import Subscribers, db

index_bp = Blueprint(
    'index_bp',
    __name__,
    template_folder='templates',
    static_folder='static'
)


@index_bp.route('/', methods=['GET', 'POST'])
def index():
    sub_form = SubscribeForm()
    form_status = request.args.get('success')

    if sub_form.validate_on_submit():
        if not sub_form.sub_18.data and not sub_form.sub_45.data:
            flash('Please select at least 1 age group')
        else:
            pincode = Pincodes.query.get(sub_form.pincode.data)

            if pincode == None:
                pincode = Pincodes(pincode=sub_form.pincode.data)
                db.session.add(pincode)

            subscriber = Subscribers(
                name=sub_form.name.data.strip(),
                email=sub_form.email.data,
                sub_18=sub_form.sub_18.data,
                sub_45=sub_form.sub_45.data,
            )
            subscriber.pincodes.append(pincode)

            db.session.add(subscriber)
            db.session.commit()

            success_msg = render_template(
                'subscribe-success-mail.html',
                user_name=subscriber.name,
                pincode=pincode.pincode,
            )
            msg = Message('Subscribied successfully for Cowin Alerts!',
                          recipients=[subscriber.email], html=success_msg)
            mail.send(msg)

            return redirect(url_for('index_bp.index', success=True))

    return render_template(
        'index.html',
        title='Cowin Alerts',
        sub_form=sub_form,
        success=form_status,
    )
