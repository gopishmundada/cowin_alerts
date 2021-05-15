import requests
import json
import datetime
import pandas as pd
import psycopg2
import time
import smtplib
s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login("vaccine.alerts.india@gmail.com", "Cowin@1234")
conn = psycopg2.connect(database="vlpaxxyk",
  user="vlpaxxyk",
  password="Hdaq9BzSKi41IA63cS-8W7xbkRCl6mKs",
  host="queenie.db.elephantsql.com",
  port="5432"
)
cur = conn.cursor()


def fetchData(pincode,date):
    api_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByPin"
    params = {
    'pincode':pincode,
    'date':date
    }
    headers = { 
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    }
    r= requests.get(url=api_url,params=params, headers=headers)
    return r 


def send_email(msg):
    message = """\
    Subject: Vaccine_Alert_Jalna

    Hello,

    Please find below details for vaccines in jalna
    """+str(msg)
    recipients = ['gopishmundada@gmail.com', 'bittumundada@gmail.com']

    # sending the mail
    s.sendmail("mundadaga@gmail.com", recipients, message)


def create_msg(base_date,jsonData):
    msg = ""
    for x in range (len(jsonData['centers'])):
        for y in range (len(jsonData['centers'][x]['sessions'])):
            avail_data+= jsonData['centers'][x]['sessions'][y]['available_capacity']
            if avail_data>0:
                x_capacity = "available_capacity: "+str(avail_data)
                x_age = "Age: "+str(jsonData['centers'][x]['sessions'][y]['min_age_limit'])+"+"
                msg = "Date:"+str(base_date)+"\n\t"+x_Location+"\n\t"+x_capacity+"\n\t"+x_age+"\n\t"+x_vaccine+"\n\n"
                print(msg)
                #send_email(msg)
                

df = pd.read_sql_query('select distinct pincode from subscribers',con=conn)
for i,row in df.iterrows():
    print(str(row['pincode']))
    base_today = (datetime.datetime.today()).strftime("%d-%m-%Y")
    data_today  = fetchData('431203',base_today)
    jsonData = data_today.json()
    print(jsonData)
    #create_msg(base_today,jsonData)