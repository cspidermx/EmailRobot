import imaplib
from flask import render_template
from emapp import app
import smtplib
from email.message import EmailMessage
import threading
import time
import re
from emapp import emrdb
from emapp.models import Service
import email
import emapp.tokenizer as Tk
import os
from bs4 import BeautifulSoup
from dateutil import parser
from dateutil.tz import gettz


def email_address(string):
    # Regular expression matching according to RFC 2822 (http://tools.ietf.org/html/rfc2822)
    rfc2822_re = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
    email_prog = re.compile(rfc2822_re, re.IGNORECASE)
    eml = email_prog.findall(string)
    if len(eml) == 0:
        return None
    else:
        return eml


class StoppableThread(threading.Thread):

    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


def readstatus():
    try:
        s = Service.query.one()
    except:
        s = Service(running=0)
        emrdb.session.add(s)
        emrdb.session.commit()
    return s


def maint(caller):
    global ab
    ab = StoppableThread(target=mainthread, args=(app, caller))
    ab.setName("maint")
    ab.daemon = True
    ab.start()


def mainthread(app, caller):
    with app.app_context():
        s = readstatus()
        if s is not None:
            if s.running:
                if caller == 1:
                    mainprocess(1)
                # for i in range(1, 10):
                i = 1
                while not ab.stopped() and i <= 10:
                    time.sleep(30)
                    i = i+1
                if not ab.stopped():
                    mainprocess(2)


def mainprocess(clr):
    imapserver = app.config['IMAP']
    con = auth(imapserver)
    r, d = con.select('INBOX')
    if r != 'OK':
        return True
    tzinfos = {"CST": gettz("America/Mexico_City")}
    # for i in range(int(b'1'), int(d[0]) + 1):
    for i in range(int(b'1'), int(d[0]) + 1):
        idmail = str(i).encode('ascii')
        result, data = con.fetch(idmail, '(RFC822)')
        raw = email.message_from_bytes(data[0][1])
        soup = BeautifulSoup(get_body(raw), 'html.parser')
        whereat = raw['From'].find("@", 0) + 1
        wheredot = raw['From'].find(".", whereat)
        cliente = raw['From'][whereat:wheredot]
        frmt = Tk.tkformat(soup.get_text())
        if frmt == 1:
            emldta = (email_address(raw['To']),
                        email_address(raw['From']),
                        raw['Subject'].replace('***SPAM***', '').strip(),
                        parser.parse(raw['Date'].replace("CST_NA", "CST"), tzinfos=tzinfos).strftime('%d-%m-%Y %H:%M:%S'),
                        cliente,
                        raw['Message-ID'])
            # .strftime('{%Y-%m-%d %H:%M:%S}')
            # dt = parser.parse(raw['Date'].replace("CST_NA", "CST"))
            # print(dt.strftime('%d-%m-%Y %H:%M:%S'))
            tokens = Tk.tknzr(soup.get_text())
            try:
                tokens[1] = parser.parse(tokens[1].replace("CST_NA", "CST"), tzinfos=tzinfos).strftime('%d-%m-%Y %H:%M:%S')
            except:
                None
            try:
                tokens[2] = parser.parse(tokens[2].replace("CST_NA", "CST"), tzinfos=tzinfos).strftime('%d-%m-%Y %H:%M:%S')
            except:
                None
            file_path = os.path.join('C:\\Users\\Charly\\Desktop\\SapMails', "emails.txt")
            if not os.path.isfile(file_path):
                mode = 'wb'
            else:
                mode = 'ab'
            with open(file_path, mode) as f:
                if mode == 'wb':
                    f.write('ID|To|From|Subject|Date|Cliente|MsgID'.encode('utf-8') + b'\r\n')
                f.write((str(i) + '|').encode('utf-8') + '|'.join(map(str, emldta)).encode('utf-8') + b'\r\n')
            file_path = os.path.join('C:\\Users\\Charly\\Desktop\\SapMails', "data.txt")
            if not os.path.isfile(file_path):
                mode = 'wb'
            else:
                mode = 'ab'
            with open(file_path, mode) as f:
                if mode == 'wb':
                    f.write('ID|Alert Details|Start Date Time|End Date Time|Managed Object|Category|Rating|Status|Description|Analysis Tools'.encode('utf-8') + b'\r\n')
                f.write((str(i) + '|').encode('utf-8') + '|'.join(map(str, tokens)).encode('utf-8') + b'\r\n')
        # file_path = os.path.join('C:\\Users\\Charly\\Desktop\\SapMails', cliente, str(idmail) + ".html")
        # with open(file_path, 'wb') as f:
        #     f.write(get_body(raw))
        print(str(i) + "/" + str(int(d[0])) + " - " + cliente + " - ")
        # print(emldta)
        # print(tokens)
        if ab.stopped():
            fin(con)
            return True
    fin(con)
    if clr != 1:
        maint(2)


def get_body(msg):  # extracts the body from the email
    if msg.is_multipart():
        return get_body(msg.get_payload(1))
    else:
        return msg.get_payload(None, True)


def auth(conf):  # sets up the auth
    conn = imaplib.IMAP4_SSL(conf['server'], conf['port'])
    conn.login(conf['user'], conf['password'])
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
    threading.Thread(target=send_async_email, args=(app, server, msg)).start()


def send_password_reset_email(usr):
    smtpserver = app.config['SMTP']

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
