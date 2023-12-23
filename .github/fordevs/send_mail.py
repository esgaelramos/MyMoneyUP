"""Script to send emails with an attached file (backup).

This script allows sending a backup file via email
using the provided credentials and Gmail's SMTP configuration.

Example:
    python send_mail.py backup_file email_user email_password recipient \
        subject body

Project Use:
    This script is run within the bash script `backup_db.sh` to send the
    backup file by email (executed in cronjob).
"""

import os
import smtplib
import argparse
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(backup_file, email_user, email_password, recipient, subject,
               body):
    """Send an email with an attached file.

    Args:
    - backup_file (str): Path of the backup file to attach.
    - email_user (str): Sender's email address.
    - email_password (str): Sender's email password.
    - recipient (str): Recipient's email address.
    - subject (str): Email subject.
    - body (str): Email body.
    """
    # Email Configuration
    FROM = email_user
    TO = recipient
    SUBJECT = subject
    BODY = body

    # Create message
    msg = MIMEMultipart()
    msg['From'] = FROM
    msg['To'] = TO
    msg['Subject'] = SUBJECT
    msg.attach(MIMEText(BODY, 'plain'))

    # Attach the backup file
    with open(backup_file, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())

        encoders.encode_base64(part)
        filename = os.path.basename(backup_file)
        content_disposition = f"attachment; filename={filename}"
        part.add_header('Content-Disposition', content_disposition)

        msg.attach(part)

    # Send the email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_password)
        server.sendmail(FROM, TO, msg.as_string())
        server.quit()
        print("Mail sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send backup file by email.")

    parser.add_argument("backup_file", help="Path of the backup file to \
                        send.")
    parser.add_argument("email_user", help="Your email address.")
    parser.add_argument("email_password", help="Your email password.")
    parser.add_argument("recipient", help="Recipient's email address.")
    parser.add_argument("subject", help="Email subject.")
    parser.add_argument("body", help="Email body.")

    args = parser.parse_args()

    send_email(args.backup_file, args.email_user, args.email_password,
               args.recipient, args.subject, args.body)
