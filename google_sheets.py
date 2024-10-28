import re
from datetime import datetime, timedelta
from pdb import set_trace as st

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

from config import DEFAULT_FOLLOW_UP_INTERVAL, SHEET_NAME, SPREADSHEET_ID

# Define the required Google Sheets API scope
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


class Customer:
    def __init__(
        self,
        name,
        first_name,
        last_name,
        email,
        email_style,
        follow_up_override=False,
        follow_up_interval=DEFAULT_FOLLOW_UP_INTERVAL,
        last_contact_date=None,
    ):

        self.name = name
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.email_style = email_style
        self.follow_up_override = follow_up_override
        self.follow_up_interval = self._parse_int(
            follow_up_interval, DEFAULT_FOLLOW_UP_INTERVAL
        )
        self.last_contact_date = self._parse_date(last_contact_date)

    def _parse_date(self, date_str):
        if date_str:
            try:
                return datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                print(
                    f"Warning: Invalid date format for customer {self.name}: {date_str}"
                )
        return None

    def _parse_int(self, value, default):
        try:
            return int(value)

        except (TypeError, ValueError):
            return default


def authenticate_google_sheets():
    try:
        creds = Credentials.from_service_account_file(
            "credentials.json", scopes=SCOPES
        )

        return build("sheets", "v4", credentials=creds).spreadsheets()

    except FileNotFoundError:
        raise RuntimeError("Credentials file 'credentials.json' not found.")

    except Exception as e:
        raise RuntimeError(f"Error authenticating with Google Sheets API: {e}")


def get_data(sheets):
    try:
        results = (
            sheets.values()
            .get(spreadsheetId=SPREADSHEET_ID, range=SHEET_NAME)
            .execute()
        )

    except Exception as e:
        raise RuntimeError(f"Error fetching data from Google Sheets: {e}")

    return results.get("values", [])


def get_customers(sheets):
    data = get_data(sheets)

    if not data:
        return []

    customers = []
    headers = data[0]

    for customer_data in data[1:]:

        data = dict(zip(headers, customer_data))

        if not is_valid_data(data):
            continue

        customer = Customer(
            name=data.get("Name"),
            first_name=data.get("firstName"),
            last_name=data.get("lastName"),
            email=data.get("Email"),
            email_style=data.get("Email Style"),
            follow_up_override=bool(data.get("Follow Up?")),
            follow_up_interval=data.get("Custom Follow-Up Interval"),
            last_contact_date=data.get("Last Contact Date"),
        )

        customers.append(customer)

    return customers


def is_valid_data(data):

    # Condition 1: Skip if all cells are empty or "FALSE"
    if all(cell == "" or cell == "FALSE" for cell in data):
        return False

    # Condition 2: Check for presence of required fields
    required_fields = ["Name", "firstName", "lastName", "Email", "Email Style"]
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


def update_last_contact_date(sheets, customer, date_str):
    data = get_data(sheets)

    if not data:
        return []

    headers = data[0]

    if "Last Contact Date" not in headers:
        raise ValueError("Could not find 'Last Contact Date' column.")

    col_index = headers.index("Last Contact Date") + 1

    for i, row in enumerate(data[1:], start=2):
        if row and row[headers.index("Email")] == customer.email:
            row_index = i
            break

    try:
        body = {"values": [[date_str]]}
        sheets.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!R{row_index}C{col_index}",
            valueInputOption="USER_ENTERED",
            body=body,
        ).execute()

    except Exception as e:
        raise RuntimeError(
            f"Error updating 'Last Contact Date' to {customer.email}: {e}"
        )
