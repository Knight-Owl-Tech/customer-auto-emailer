import re
from datetime import datetime, timedelta


def is_valid_data(data):

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
    if not last_contact_date:
        return True

    today = datetime.now().date()
    return (last_contact_date + timedelta(days=interval)) <= today
