from pdb import set_trace as st

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

from config import SHEET_NAME, SPREADSHEET_ID

# Define the required Google Sheets API scope
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


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

    # Fetch customer data from the specified range
    result = (
        sheet.values()
        .get(spreadsheetId=SPREADSHEET_ID, range=SHEET_NAME)
        .execute()
    )
    rows = result.get("values", [])

    if not rows:
        print("No data found in the sheet.")
        return []

    # Convert data to list of dictionaries if headers are included
    headers = rows[0]  # assuming first row contains headers
    customers = [dict(zip(headers, row)) for row in rows[1:]]

    return customers
