import smtplib, ssl
import configparser


gmail_user = 'kevdav394'
gmail_password = 'whatIsjudy12345'

#email properties
sent_from = gmail_user
to = ['kevdav394@gmail.com']
subject = 'Alert for reduced in price'
email_text = \
"""
Alert for reduced in price
"""

# email send request
try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()
    print ('Email sent!')
except Exception as e:
    print(e)
    print ('Something went wrong...')
