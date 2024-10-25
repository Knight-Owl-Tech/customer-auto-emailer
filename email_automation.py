import os
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from pdb import set_trace as st

from config import EMAIL_ADDRESS, EMAIL_PASSWORD
from google_sheets import get_customer_data

# Constants for the follow-up logic
FOLLOW_UP_INTERVAL_DAYS = 7  # Example: follow up after 7 days


def should_send_follow_up(last_contact_date, interval=FOLLOW_UP_INTERVAL_DAYS):
    """Check if a follow-up email should be sent based on the last contact date."""
    today = datetime.now().date()
    return last_contact_date + timedelta(days=interval) <= today


def send_email(recipient, subject, body):
    """Send an email to a customer."""
    msg = MIMEText(body, "html")
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = recipient
    msg["Subject"] = subject

    try:
        # Connect to SMTP server and send email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, recipient, msg.as_string())
            print(f"Email sent to {recipient}")
    except Exception as e:
        print(f"Error sending email to {recipient}: {e}")


def get_email_content(customer_name):
    """Generate the email body based on a template."""
    with open(
        os.path.join("templates", "followup_template.html"), "r"
    ) as template_file:
        content = template_file.read()
        return content.replace("{{ customer_name }}", customer_name)


def main():
    """Main function to automate the email follow-up process."""
    customers = get_customer_data()

    for customer in customers:
        name, email, last_contact_str = (
            customer["Name"],
            customer["Email"],
            customer["Last Contact Date"],
        )
        last_contact_date = datetime.strptime(
            last_contact_str, "%Y-%m-%d"
        ).date()

        if should_send_follow_up(last_contact_date):
            email_body = get_email_content(name)
            send_email(email, f"Follow-up from {EMAIL_ADDRESS}", email_body)


if __name__ == "__main__":
    main()
