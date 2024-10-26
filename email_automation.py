import os
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from pdb import set_trace as st

from config import EMAIL_ADDRESS, EMAIL_PASSWORD
from google_sheets import get_customer_data, update_last_contact_date


def should_follow_up(last_contact_date, interval):
    """Determine if a follow-up email is due based on last contact date and interval."""
    if not last_contact_date:
        return False

    today = datetime.now().date()
    return (last_contact_date + timedelta(days=interval)) <= today


def send_email(customer, body):
    """Send an email to a customer."""
    msg = MIMEText(body, "html")
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = customer.email
    msg["Subject"] = "Follow-Up Email"

    try:
        # Connect to SMTP server and send email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, customer.email, msg.as_string())
            print(f"Email sent to {customer.email}")
        return True

    except Exception as e:
        print(f"Error sending email to {customer.email}: {e}")
        return False


def create_email_content(customer):
    """Generate the email body based on a template."""
    template_mapping = {
        "Formal": "formal_follow-up.html",
        "Casual": "casual_follow-up.html",
    }

    try:
        template = template_mapping.get(customer.email_style)

    except Exception as e:
        print(f"Email Style is missing for {customer.name}")

    try:
        with open(os.path.join("templates", template), "r") as template_file:
            content = template_file.read()
            return content.replace("{{ customer_name }}", customer.first_name)
    except FileNotFoundError:
        print(f"Template not found: {template}")


def main():

    customers = get_customer_data()

    for customer in customers:
        if should_follow_up(
            customer.last_contact_date, customer.follow_up_interval
        ):

            email_body = create_email_content(customer)

            if send_email(customer, email_body):
                date_str = datetime.now().strftime("%Y-%m-%d")
                update_last_contact_date(customer.row_number, date_str)


if __name__ == "__main__":
    main()
