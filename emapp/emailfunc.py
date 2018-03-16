import imaplib
import smtplib
from email.message import EmailMessage
import datetime
import re


def auth(usr, pwd, imapurl):  # sets up the auth
    conn = imaplib.IMAP4_SSL(imapurl, 993)
    conn.login(usr, pwd)
    return conn


def fin(cnn):  # closes the folder and terminates the connection
    cnn.close()
    cnn.logout()


def send_password_reset_email(usr):
    msg = EmailMessage()
    msg['Subject'] = "Restablecer Password - Robot Email"
    msg['From'] = "me"
    msg['To'] = "You"
    smtp = smtplib.SMTP(cfig['server'], cfig['port'])
    smtp.starttls()
    # smtp = smtplib.SMTP_SSL(cfig['server'], cfig['port'])  # Use this for Nemaris Server
    smtp.login(cfig['user'], cfig['password'])
    smtp.sendmail('deepcri77@gmail.com', 'cbarajas@carant-games.com', message.as_string())
    smtp.quit()
