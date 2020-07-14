import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


print("email file imported")
#remember to set these env vars in heroku
if os.environ.get("RECEIVER_EMAIL") != None:
    RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL")
    EMAIL_ACC = os.environ.get("EMAIL_ACC")
    PASSWORD = os.environ.get("PASSWORD")
    print("HEROKU KEY STORAGE")
else:
    from env import keys
    print("LOCAL KEY STORAGE")

        
def visitalert(visinfo):

    server = smtplib.SMTP('smtp.mail.com', 587)

    user = keys.EMAIL_ACC
    password = keys.PASSWORD

    fromaddr = keys.EMAIL_ACC
    toaddr = keys.RECEIVER_EMAIL

    msg = MIMEMultipart()

    msg['From'] = f'Wobot <{fromaddr}>'
    msg['To'] = toaddr
    msg['Subject'] = 'Website Visitor Alert'

    msgbody = 'Message: \n\n Site Visit\n\n Visitor Details:\n\n'

    for key, info in visinfo.items():
        msgbody = msgbody + str(key) + ': ' + str(info) + ' \n'

    msgbody = msgbody + '\n\n\nFrom Wobot'
    
    msg.attach(MIMEText(msgbody, 'plain'))

    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(user, password)
    text = msg.as_string()
    print("EMAILER: SENDING")
    server.sendmail(fromaddr, toaddr, text)
    print("EMAILER: SENT")
    server.close()
    print("EMAILER: CLOSED")









    # def msgbuilder(visinfo):
        # ip = visinfo['IP']
        # isp = visinfo['ISP']
        # provider = visinfo['Provider']
        # provider_site = visinfo['Provider_site']
        # region = visinfo['Region']
        # country = visinfo['Country']
        # city = visinfo['City']
        # lat = visinfo['Latitude']
        # lng = visinfo['Longitude']
        # os = visinfo['OS'] 
        # user_agent = visinfo['User_Agent'] 
        # client = visinfo['Client'] 
        # device_data = visinfo['Device_Data']
        # device = visinfo['Device'] 
        # visitor_local_time = visinfo['Visit_Time_Local']
        # istor = visinfo['Tor'] 
        # isproxy = visinfo['Proxy'] 
        # isanon = visinfo['Anonymous']
        # isthreat = visinfo['Is_threat']

