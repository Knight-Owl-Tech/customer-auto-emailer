from datetime import datetime, timedelta
from pdb import set_trace as st

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

from config import DEFAULT_FOLLOW_UP_INTERVAL, SHEET_NAME, SPREADSHEET_ID

# Define the required Google Sheets API scope
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


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
        """Convert date string to a datetime.date object, or None if empty."""
        if date_str:
            try:
                return datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                print(
                    f"Warning: Invalid date format for customer {self.name}: {date_str}"
                )
        return None

    def _parse_int(self, value, default):
        """Safely parse an integer with a fallback default."""
        try:
            return int(value)

        except (TypeError, ValueError):
            return default


def get_google_sheets_service():
    """Authenticate and return a Google Sheets service instance."""
    creds = Credentials.from_service_account_file(
        "credentials.json", scopes=SCOPES
    )

    return build("sheets", "v4", credentials=creds)


def get_customer_data():
    """Fetch customer data from Google Sheets."""
    service = get_google_sheets_service()
    sheet = service.spreadsheets()

    try:
        # Fetch customer data from the specified range
        result = (
            sheet.values()
            .get(spreadsheetId=SPREADSHEET_ID, range=SHEET_NAME)
            .execute()
        )
        rows = result.get("values", [])

    except Exception as e:
        print(f"Error fetching data from Google Sheets: {e}")
        return []

    if not rows:
        print("No data found from Google Sheets.")
        return []

    customers = []
    headers = rows[0]  # assuming first row contains headers

    for row in rows[1:]:

        data = dict(zip(headers, row))

        try:

            customer = Customer(
                name=data.get("Name"),
                first_name=data.get("firstName"),
                last_name=data.get("lastName"),
                email=data.get("Email"),
                email_style=data.get("Email Style"),
                follow_up_override=data.get("Follow Up?"),
                follow_up_interval=data.get("Custom Follow-Up Interval"),
                last_contact_date=data.get("Last Contact Date"),
            )

            customers.append(customer)

        except Exception as e:
            print(f"Error creating customer from row data {data}: {e}")

    return customers


def update_last_contact_date(row_number, date_str):
    """Update the 'Last Contact Date' for a specific row in Google Sheets."""
    service = get_google_sheets_service()
    try:
        body = {"values": [[date_str]]}
        range_to_update = f"{SHEET_NAME}!I{row_number}"  # Assuming "Last Contact Date" is column I
        service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=range_to_update,
            valueInputOption="USER_ENTERED",
            body=body,
        ).execute()
        print(
            f"Updated 'Last Contact Date' for row {row_number} to {date_str}"
        )
    except Exception as e:
        print(f"Error updating 'Last Contact Date' for row {row_number}: {e}")
