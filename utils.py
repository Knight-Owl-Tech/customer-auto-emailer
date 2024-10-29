import re
from datetime import datetime, timedelta


def is_valid_data(data):
    """
    Validates a dictionary of customer data based on specific conditions:
    1. Ensures that at least one cell contains meaningful data.
    2. Verifies the presence of required fields: "Email" and "Email Style".
    3. Checks that the email format is valid.

    Parameters:
        data (dict): A dictionary containing customer data with field names as keys.

    Returns:
        bool: True if the data is valid based on the above criteria, otherwise False.
    """

    # Condition 1: Skip if all cells are empty or "FALSE"
    if all(cell == "" or cell == "FALSE" for cell in data):
        return False

    # Condition 2: Check for presence of required fields
    required_fields = ["Email", "Email Style"]
    missing_fields = [
        field for field in required_fields if not data.get(field)
    ]

    if missing_fields:
        return False

    # Condition 3: Validate email format
    email = data.get("Email")
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_pattern, email):
        return False

    return True


def should_follow_up(last_contact_date, interval):
    """
    Determines if a follow-up is due based on the last contact date and follow-up interval.

    Parameters:
        last_contact_date (datetime.date or None): The last date of customer contact.
        interval (int): The interval in days after which a follow-up is needed.

    Returns:
        bool: True if a follow-up is due (either no previous contact date or interval elapsed), otherwise False.
    """

    if not last_contact_date:
        return True

    today = datetime.now().date()
    return (last_contact_date + timedelta(days=interval)) <= today
