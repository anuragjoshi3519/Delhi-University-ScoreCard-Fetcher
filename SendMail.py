import requests
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
