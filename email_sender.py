#!/usr/bin/env python3.6.5
import os
import getpass
import datetime
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

import email_configuration


def sending_screen_shot():
    try:
        current_date = datetime.date.today()
        user_name = getpass.getuser()
        msg = MIMEMultipart()
        msg['From'] = email_configuration.EMAIL_ADDRESS
        msg['To'] = email_configuration.RECIPIENT_ADDRESS
        msg['Subject'] = 'Screen-shot {}'.format(current_date)

        body = "This is a screen-shot, sent from {}'s computer, on {}".format(user_name, current_date)
        msg.attach(MIMEText(body, 'plain'))

        filename = os.path.abspath(os.path.join('.', 'ExportData', 'screenshot.bmp'))
        attachment = open(filename, 'rb')

        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= " + filename)

        msg.attach(part)
        text = msg.as_string()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(user=email_configuration.EMAIL_ADDRESS,
                     password=email_configuration.PASSWORD)

        server.sendmail(email_configuration.EMAIL_ADDRESS,
                        email_configuration.RECIPIENT_ADDRESS,
                        text)
        server.quit()
        return 1

    except Exception as ex:
        return "Unexpected error occurred. Details: {}".format(ex)
