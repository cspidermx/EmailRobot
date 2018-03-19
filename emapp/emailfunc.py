import imaplib
from flask import render_template
from emapp import app
import smtplib
from email.message import EmailMessage
from threading import Thread
import datetime
import re


def auth(usr, pwd, imapurl):  # sets up the auth
    conn = imaplib.IMAP4_SSL(imapurl, 993)
    conn.login(usr, pwd)
    return conn


def fin(cnn):  # closes the folder and terminates the connection
    cnn.close()
    cnn.logout()


def send_async_email(app, srv, msge):
    with app.app_context():
        if not srv['SSL']:
            smtp = smtplib.SMTP(srv['server'], srv['port'])
            smtp.starttls()
        else:
            smtp = smtplib.SMTP_SSL(srv['server'], srv['port'])  # Use this for Nemaris Server
        smtp.login(srv['user'], srv['password'])
        smtp.sendmail(msge['From'], msge['To'], msge.as_string())
        smtp.quit()


def send_email(server, msg):
    Thread(target=send_async_email, args=(app, server, msg)).start()


def send_password_reset_email(usr):
    smtpserver = app.config['SMTPGOOGLE']
    # smtpserver = app.config['SMTPNEMARIS']

    msg = EmailMessage()
    msg['Subject'] = "Restablecer Password - Robot Email"
    msg['From'] = smtpserver['user']
    msg['To'] = usr.email
    msg.set_type('text/html')

    token = usr.get_reset_password_token()
    msg.set_content(render_template('email/reset_password.txt', user=usr, token=token))
    html_msg = render_template('email/reset_password.html', user=usr, token=token)
    msg.add_alternative(html_msg, subtype="html")

    send_email(smtpserver, msg)
    #  print(msg)
