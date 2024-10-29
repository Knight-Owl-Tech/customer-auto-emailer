from pdb import set_trace as st

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

from config import SHEET_NAME, SPREADSHEET_ID
from models import Customer
from utils import is_valid_data

# Define the required Google Sheets API scope
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def authenticate_google_sheets():
    """
    Authenticates and returns a Google Sheets service object.

    Returns:
        googleapiclient.discovery.Resource: The authenticated Google Sheets service object.

    Raises:
        RuntimeError: If the credentials file is not found or if there is an error during authentication.
    """

    try:
        creds = Credentials.from_service_account_file(
            "credentials.json", scopes=SCOPES
        )

        return build("sheets", "v4", credentials=creds).spreadsheets()

    except FileNotFoundError:
        raise RuntimeError("Credentials file 'credentials.json' not found.")

    except Exception as e:
        raise RuntimeError(f"Error authenticating with Google Sheets API: {e}")


def fetch_sheet_data(sheets):
    """
    Fetches data from the specified Google Sheet.

    Args:
        sheets (googleapiclient.discovery.Resource): The authenticated Google Sheets service object.

    Returns:
        list: A list of values retrieved from the Google Sheet.

    Raises:
        RuntimeError: If there is an error fetching data from the Google Sheets.
    """

    try:
        results = (
            sheets.values()
            .get(spreadsheetId=SPREADSHEET_ID, range=SHEET_NAME)
            .execute()
        )

    except Exception as e:
        raise RuntimeError(f"Error fetching data from Google Sheets: {e}")

    return results.get("values", [])


def load_customers(sheets):
    """
    Loads customers from the Google Sheet and returns a list of Customer objects.

    Args:
        sheets (googleapiclient.discovery.Resource): The authenticated Google Sheets service object.

    Returns:
        list: A list of Customer objects populated from the sheet data.
    """

    data = fetch_sheet_data(sheets)

    if not data:
        return []

    customers = []
    headers = data[0]

    for customer_data in data[1:]:

        data = dict(zip(headers, customer_data))

        if not is_valid_data(data):
            continue

        customer = Customer(
            email=data.get("Email"),
            email_style=data.get("Email Style"),
            first_name=data.get("First Name"),
            last_name=data.get("Last Name"),
            company=data.get("Company"),
            enable_follow_up=bool(data.get("Follow Up?")),
            follow_up_interval=data.get("Custom Follow-Up Interval"),
            last_contact_date=data.get("Last Contact Date"),
        )

        customers.append(customer)

    return customers


def update_last_contact_date(sheets, customer, date_str):
    """
    Updates the 'Last Contact Date' for a specific customer in the Google Sheet.

    Args:
        sheets (googleapiclient.discovery.Resource): The authenticated Google Sheets service object.
        customer (Customer): The customer whose last contact date is to be updated.
        date_str (str): The new contact date in "YYYY-MM-DD" format.

    Raises:
        ValueError: If the 'Last Contact Date' column is not found.
        RuntimeError: If there is an error updating the last contact date.
    """

    data = fetch_sheet_data(sheets)

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
            f"Error updating 'Last Contact Date' for {customer.recipient_name}: {e}"
        )
