import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from pdb import set_trace as st

from config import EMAIL_ADDRESS, EMAIL_PASSWORD
from google_sheets import (
    authenticate_google_sheets,
    load_customers,
    update_last_contact_date,
)
from utils import should_follow_up


def send_email(customer, body):
    """
    Sends an email to the specified customer.

    Args:
        customer (Customer): The customer object containing email details.
        body (str): The HTML content of the email.

    Raises:
        RuntimeError: If there is an error during the SMTP process or sending the email.
    """

    msg = MIMEText(body, "html")
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = customer.email
    msg["Subject"] = "Follow-Up Email"

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, customer.email, msg.as_string())

    except smtplib.SMTPException as e:
        raise RuntimeError(
            f"SMTP error sending email to {customer.email}: {e}"
        )


def create_email_content(customer):
    """
    Creates the email content for a customer based on their email style.

    Args:
        customer (Customer): The customer object containing email style and recipient details.

    Returns:
        str: The email content with the recipient's name replaced.

    Raises:
        FileNotFoundError: If the email template file is not found.
    """

    template_mapping = {
        "Formal": "formal_follow-up.html",
        "Casual": "casual_follow-up.html",
    }

    template = template_mapping.get(customer.email_style)

    try:
        with open(os.path.join("templates", template), "r") as template_file:
            content = template_file.read()
            return content.replace(
                "{{ recipient_name }}", customer.recipient_name
            )
    except FileNotFoundError:
        raise FileNotFoundError(f"Template not found: {template}")


def main():
    """
    Main function to authenticate Google Sheets, load customers,
    send follow-up emails, and update the last contact date.

    This function tracks the number of emails sent and provides feedback.
    """

    sheets = authenticate_google_sheets()

    customers = load_customers(sheets)
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
