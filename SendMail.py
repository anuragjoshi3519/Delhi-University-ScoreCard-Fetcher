from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders

import smtplib

def sendMail(fromaddr,password,toaddr,filepath):
    
    msg = MIMEMultipart() 
   
    msg['From'] = fromaddr  
    msg['To'] = toaddr

    msg['Subject'] = "Your Result"

    body = "Find the attachment."

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
        print('Mail Error!')
