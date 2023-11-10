import streamlit as st
import smtplib
from dotenv import load_dotenv
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

load_dotenv()
mail_pass = os.getenv("EMAIL_PASS")

def mail(from_name, from_addr, to_addrs, mssg, attachment):
    msg = MIMEMultipart()
    msg['From'] = f"{from_name} <{from_addr}>"
    msg['To'] = to_addrs
    msg['Subject'] = 'Subject'
    msg.attach(MIMEText(mssg, 'plain'))

    if attachment is not None:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % attachment.name)
        msg.attach(part)

    server = smtplib.SMTP("mail.creatorghost.com", 587)
    server.starttls()
    server.login("aditya@creatorghost.com", mail_pass)
    text = msg.as_string()
    server.sendmail(from_addr, to_addrs, text)
    server.quit()

st.title('Email Sender App')

from_name = st.text_input('Enter sender name:')
from_addr = st.text_input('Enter sender email:')
to_addr = st.text_input('Enter receiver email:')
subject = st.text_input('Enter email subject:')
message_content = st.text_area('Enter email content:')
attachment = st.file_uploader('Choose a file')

if st.button('Send Email'):
    message = f"""From: {from_name} <{from_addr}>
    To: {to_addr}
    Subject: {subject}
    {message_content}
    """
    mail(from_name, from_addr, to_addr, message, attachment)
    st.success('Email sent successfully.')