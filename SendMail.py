import requests
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders

from config import MAILGUN_APIKEY, MAILGUN_DOMAIN

def sendMail(toaddr,filepath):
    return requests.post(
		f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
		auth=("api", f"{MAILGUN_APIKEY}"),
        files=[("attachment", (filepath.split('/')[1], open(filepath,"rb").read()))],
		data={"from": f"DU Scorecard Fetcher <mailgun@{MAILGUN_DOMAIN}>",
			"to": [toaddr],
			"subject": "Your Result",
			"text": "Please find the attachment."})


def sendMailSMTP(fromaddr,password,toaddr,filepath):
    
    msg = MIMEMultipart() 
   
    msg['From'] = fromaddr  
    msg['To'] = toaddr

    msg['Subject'] = "Your Result"

    body = "Please find the attachment."

    msg.attach(MIMEText(body, 'plain')) 

    attachment = open(filepath, "rb") 

    p = MIMEBase('application', 'octet-stream') 

    p.set_payload((attachment).read()) 

    encoders.encode_base64(p) 

    p.add_header('Content-Disposition', "attachment; filename= %s" % filepath.split('/')[1]) 
    
    msg.attach(p) 

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        server.login(fromaddr, password)

        server.sendmail(fromaddr,toaddr, msg.as_string())
        server.quit()

        print('Mail Sent')
        
    except:
        print("Mail Error! (Make sure to allow 'less secure apps' in your gmail account)")