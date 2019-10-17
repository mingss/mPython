# -*- coding: utf-8 -*-
# -*- coding: euc-kr -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

def mailsend():
    server = "smtp.office365.com"
    port = 587
    user = "minsu.kim@cdnetworks.biz"
    pwd = ""

    title = "Hi!"
    text = "이거 파이썬으로 보내는거에요! :)"
    sender = "minsu.kim2@cdnetworks.com"
    receiver = "yeojin.jeong@cdnetworks.com, minsu.kim2@cdnetworks.com"
    msg = MIMEMultipart()
    msg['From'] = user
    msg['To'] = receiver
    msg['Subject'] = title
    msg.attach(MIMEText(text))
    smtp = smtplib.SMTP(server, port)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(user, pwd)
    smtp.sendmail(user, receiver, msg.as_string())
    smtp.close()



