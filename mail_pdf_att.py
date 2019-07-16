# Licensed under the MIT license
# Copyright (c) 2016 Yves Van Belle (yvanbelle@brother.be)

import smtplib
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def mail_with_pdf(email_server, from_email_address, to_email_address, email_subject, attachment, email_body):
    try:
        pdf_file = open(attachment, 'rb')
        pdf = MIMEApplication(pdf_file.read())
        pdf.add_header('content-disposition', 'attachment', filename=basename(attachment))

        text = MIMEText(email_body, _charset='UTF-8')

        msg = MIMEMultipart(_subparts=(text, pdf))
        msg['Subject'] = email_subject
        msg['From'] = from_email_address
        msg['To'] = to_email_address

        s = smtplib.SMTP(email_server)
        s.send_message(msg)
        s.quit()
    except FileNotFoundError:
        pass


if __name__ == '__main__':
    email_server = 'bbesmtp.eu.brothergroup.net'
    from_email_address = 'brother.bsi@brother.be'
    to_email_address = 'yvanbelle@brother.be'
    email_subject = 'Send email with PDF attachment'
    attachment = r'c:\Users\belleyve\Desktop\Supplies.pdf'
    email_body = '''BSI email with PDF attachment

Scan with BSI to file, then send email from server with PDF attachment.'''

    mail_with_pdf(email_server, from_email_address, to_email_address, email_subject, attachment, email_body)
