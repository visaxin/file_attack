#!/usr/bin/python

import smtplib
import sys
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os

gmail_user = "1474739840@qq.com"
#gmail_pwd = "******"
gmail_pwd = "admin1962"
def mail(to, subject, text, attach):
   msg = MIMEMultipart()

   msg['From'] = gmail_user
   msg['To'] = to
   msg['Subject'] = subject

   msg.attach(MIMEText(text))


   for f in attach:
    #open with 'rb' to read non-text file
       with open(f,'rb') as f_attach:
           part = MIMEBase('application', 'octet-stream')
           part.set_payload(f_attach.read())
           Encoders.encode_base64(part)
           part.add_header('Content-Disposition',
                            'attachment; filename=""%s"' %os.path.basename(f))
           msg.attach(part)
   try:

       mailServer = smtplib.SMTP("smtp.qq.com")
       mailServer.login(gmail_user, gmail_pwd)
       mailServer.sendmail(gmail_user, to, msg.as_string().encode('utf-8'))
       mailServer.close()
   except KeyboardInterrupt:
       sys.exit()
   # Should be mailServer.quit(), but that crashes...
