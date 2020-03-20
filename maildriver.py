import smtplib, socket
import datetime
# ENV file
from dotenv import load_dotenv
# env
from os import environ

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def read_template(filename):
    """
    Returns a Template object comprising the contents of the 
    file specified by filename.
    """
    
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def send_email(from_, to_, subject, context):
    try: 
        # smtp configurations
        smpt_host = environ.get('SMPT_HOST')
        smpt_port = environ.get('SMPT_PORT')
        s = smtplib.SMTP(host=smpt_host, port=smpt_port)
        s.starttls()
        s.login(environ.get('SMPT_USERNAME'), environ.get('SMPT_PASSWORD'))

        # message config
        msg = MIMEMultipart()
        msg['From'] = from_
        msg['To'] = to_
        msg['Subject'] = subject
        msg.attach(context)
        s.send_message(msg)
        del msg
        s.quit()
    except socket.error as e:
        print("could not connect")

def send_database_connection_error():
    subject = "Internal-Scheduled Job Error - DB connection error"

    # configure mail template
    message_template = read_template('./mail_templates/error_template.html')
    error_name = "Database Connection Error"
    job_name = "Joblist Scrapping"
    error_message = "unable to connect to the database"
    job_date = datetime.datetime.now()
    message = message_template.substitute(
        ERROR_NAME=error_name,
        JOB_NAME=job_name, 
        JOB_DATE=job_date, 
        ERROR_MESSAGE=error_message)
    context = MIMEText(message, 'html')
    send_email("guru.softwaremaster@gmail.com", "Helpdesk@sohodragon.com", subject, context)

def send_table_update_error():
    subject = "Internal-Scheduled Job Error - Updating Table Error"

    # configure mail template
    message_template = read_template('./mail_templates/error_template.html')
    error_name = "Table Update Error"
    job_name = "Joblist Scrapping"
    error_message = "Error while updating table!"
    job_date = datetime.datetime.now()
    message = message_template.substitute(
        ERROR_NAME=error_name,
        JOB_NAME=job_name, 
        JOB_DATE=job_date, 
        ERROR_MESSAGE=error_message)
    context = MIMEText(message, 'html')
    send_email(environ.get("MAIL_FROM"), environ.get("MAIL_TO"), subject, context)

def send_job_run_alert():
    subject = "InternalJob working-<Joblist scrapping> No action Required DELETE"
    
    # configure mail template
    message_template = read_template('./mail_templates/alert_template.html')
    alert_name = "Scrapping Completed"
    job_name = "Joblist Scrapping"
    job_date = datetime.datetime.now()
    message = message_template.substitute(
        ALERT_NAME=alert_name,
        JOB_NAME=job_name, 
        JOB_DATE=job_date)
    context = MIMEText(message, 'html')
    send_email(environ.get("MAIL_FROM"), environ.get("MAIL_TO"), subject, context)

if __name__ == '__main__':
    load_dotenv('.env')
    send_database_connection_error()
    send_table_update_error()
    send_job_run_alert()
