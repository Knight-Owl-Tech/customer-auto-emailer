from datetime import datetime

from config import DEFAULT_FOLLOW_UP_INTERVAL


class Customer:
    def __init__(
        self,
        email,
        email_style,
        first_name=None,
        last_name=None,
        company=None,
        enable_follow_up=False,
        follow_up_interval=DEFAULT_FOLLOW_UP_INTERVAL,
        last_contact_date=None,
    ):

        self.email = email
        self.email_style = email_style
        self.first_name = first_name
        self.last_name = last_name
        self.company = company
        self.enable_follow_up = enable_follow_up
        self.follow_up_interval = self._parse_int(follow_up_interval)
        self.last_contact_date = self._parse_date(last_contact_date)

    @property
    def name(self):
        # Use "First Last" if available, otherwise fallback to name (company name)
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return None

    @property
    def recipient_name(self):
        # property used to address the recipient in the email
        if self.name:
            if self.email_style == "Formal":
                return self.name
            return self.first_name
        return self.company

    def _parse_date(self, date_str):
        if date_str:
            try:
                return datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                print(
                    f"Warning: Invalid date format for customer {self.name}: {date_str}"
                )
        return None

    def _parse_int(self, value):
        return int(value)
