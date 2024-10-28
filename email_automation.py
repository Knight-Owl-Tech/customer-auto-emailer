import os
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from pdb import set_trace as st

from config import EMAIL_ADDRESS, EMAIL_PASSWORD
from google_sheets import (
    authenticate_google_sheets,
    get_customers,
    update_last_contact_date,
)


def should_follow_up(last_contact_date, interval):
    if not last_contact_date:
        return True

    today = datetime.now().date()
    return (last_contact_date + timedelta(days=interval)) <= today


def send_email(customer, body):
    msg = MIMEText(body, "html")
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = customer.email
    msg["Subject"] = "Follow-Up Email"

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, customer.email, msg.as_string())

    except Exception as e:
        raise RuntimeError(f"Error sending email to {customer.name}: {e}")


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

    sheets = authenticate_google_sheets()

    customers = get_customers(sheets)
    emails_sent = 0

    for customer in customers:
        if should_follow_up(
            customer.last_contact_date, customer.follow_up_interval
        ):

            email_body = create_email_content(customer)

            send_email(customer, email_body)
            update_last_contact_date(
                sheets,
                customer,
                datetime.now().strftime("%Y-%m-%d"),
            )
            emails_sent += 1

    if emails_sent == 0:
        print("No follow-up emails were sent today.")
    else:
        print(f"{emails_sent} follow-up emails sent.")


if __name__ == "__main__":
    main()
