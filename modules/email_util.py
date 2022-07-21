import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(email_template, from_email_pass):
    """
    send emails
    :param email_template: env configurations
    :return: none
    """

    to_notify_emails = email_template["to"]
    from_email = email_template["from"]

    if not from_email:
        err_msg = "From Email is not invalid. Could not send email. Pleas check email address."
        print(err_msg)
        return
    if not to_notify_emails:
        err_msg = "To Notify Emails is not invalid"
        print(err_msg)
        to_notify_emails = ""

    message = MIMEMultipart()
    message["From"] = from_email
    message["To"] = to_notify_emails
    subject = email_template["subject"]
    message["Subject"] = subject
    body = email_template["body"]
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP('smtp.gmail.com:587') as server:
        server.ehlo()
        server.starttls()
        server.login(from_email, from_email_pass)
        server.sendmail(from_email, to_notify_emails, message.as_string())
        server.quit()
