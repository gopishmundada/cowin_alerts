from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app
from ..models import Pincodes, db
from datetime import datetime
import requests
import json
import pandas as pd
import psycopg2
import time
import smtplib
s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login("vaccine.alerts.india@gmail.com", "")

def scheduled_job():
    #print(f'======> Job run:')
    pass


scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(scheduled_job, 'interval',
                  seconds=current_app.config.get('ALERT_INTERVAL'))



def fetchData(pincode,date):
    api_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
    params = {
    'pincode':pincode,
    'date':date
    }
    headers = { 
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    }
    print(pincode)
    r= requests.get(url=api_url,params=params, headers=headers)
    print(r)
    return r


def send_email(pin_code,age_grp,avail_slots,recipients):
    exe_msg = str(pin_code)+"\n"+"Age group - "+str(age_grp)+"\n"+"Slots available - "+str(avail_slots)


    message = """\
	Subject: Vaccine_Alert_Jalna

	Hello,
	Please find below details for vaccines
    
	pincode - """+exe_msg
    print(message)
    # sending the mail
    s.sendmail("vaccine.alerts.india@gmail.com", recipients, message)


def create_msg(jsonData,i):
    avail_data_45=avail_data_18=0
    for x in range (len(jsonData['centers'])):
        for y in range (len(jsonData['centers'][x]['sessions'])):
            if jsonData['centers'][x]['sessions'][y]['min_age_limit'] == 45:
                avail_data_45+= jsonData['centers'][x]['sessions'][y]['available_capacity']
            else:
            	avail_data_18+= jsonData['centers'][x]['sessions'][y]['available_capacity']
            #send_email(msg)'''
    if avail_data_18 > 0:
    	i.last_mail_sent_on = datetime.now()
    	recipients = [u.email for u in i.subscribers if u.sub_18]
    	send_email(i.pin_code,"18+",avail_data_18,recipients)
    if avail_data_45 >= 0:
    	i.last_mail_sent_on = datetime.now()
    	recipients = [u.email for u in i.subscribers if u.sub_45]
    	send_email(i.pincode,"45+",avail_data_45,recipients)

    db.session.commit()

def test_date():
    pincode = Pincodes.query.all()

    for i in pincode:
    	print("Hii")
    	if i.last_mail_sent_on == None or ((datetime.now() - i.last_mail_sent_on).total_seconds() / 60) > 30:
	        base_today = (datetime.today()).strftime("%d-%m-%Y")
	        data_today  = fetchData(i.pincode, base_today)
	        jsonData = data_today.json()
	        create_msg(jsonData,i)