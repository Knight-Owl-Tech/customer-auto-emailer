import configparser
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

config = configparser.ConfigParser()
config.read(f"{BASE_DIR}/email.cfg")

SPREADSHEET_ID = config.get("google_sheets", "spreadsheet_id")

SHEET_NAME = config.get("google_sheets", "sheet_name", fallback="Sheet1")

EMAIL_ADDRESS = config.get("smtp_settings", "email_address")

EMAIL_PASSWORD = config.get("smtp_settings", "email_password")

DEFAULT_FOLLOW_UP_INTERVAL = int(
    config.get("email_automation", "default_follow_up_interval")
)
