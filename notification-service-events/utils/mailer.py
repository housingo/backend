import smtplib
from email.message import EmailMessage
import os

# from db import get_emails
from .email_template import listingTemplate, welcomeTemplate

smtp_server = "smtp.hostinger.com"
sender_email = "info@housingo.nl"  # Enter your address
password = os.environ.get("EMAIL_PASSWORD")
email = EmailMessage()

email["From"] = "info@housingo.nl"


def mail_listing(linkToApartment, email_list):

    for mail in email_list:
        email["Subject"] = "A new listing is available"
        email["BCC"] = mail
        email.set_content(listingTemplate(linkToApartment), subtype="html")
        server = smtplib.SMTP(host=smtp_server, port=587)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(email)
        server.quit()
        del email["To"], email["Subject"], email["BCC"]


def mail_welcome(email_list):

    for mail in email_list:
        email["Subject"] = "Welcome to Housingo!"
        email["BCC"] = mail
        email.set_content(welcomeTemplate(), subtype="html")
        server = smtplib.SMTP(host=smtp_server, port=587)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(email)
        server.quit()
        del email["To"], email["Subject"], email["BCC"]
