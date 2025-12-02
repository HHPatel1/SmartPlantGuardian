
import smtplib
from email.message import EmailMessage

def send_alert(to, subject, message):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = "smartplantlabs@outlook.com"
    msg["To"] = to
    msg.set_content(message)

    with smtplib.SMTP("smtp-mail.outlook.com", 587) as s:
        s.starttls()
        s.login("smartplantlabs@outlook.com", "YOUR_PASSWORD")
        s.send_message(msg)

