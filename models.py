from datetime import datetime

from config import DEFAULT_FOLLOW_UP_INTERVAL


class Customer:
    """
    Represents a customer with attributes related to follow-up email preferences, contact details,
    and follow-up interval. Provides functionality for parsing and formatting customer information.

    Attributes:
        email (str): The customer's email address.
        email_style (str): Style of email communication ("Formal" or "Casual").
        first_name (str, optional): The customer's first name. Default is None.
        last_name (str, optional): The customer's last name. Default is None.
        company (str, optional): The company associated with the customer. Default is None.
        enable_follow_up (bool): Flag indicating if follow-up emails are enabled. Default is False.
        follow_up_interval (int): The number of days between follow-ups, parsed as an integer.
        last_contact_date (datetime.date): The date of the last email contact. Default is None.
    """

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
        self.follow_up_interval = int(self._parse_int(follow_up_interval))
        self.last_contact_date = self._parse_date(last_contact_date)

    @property
    def name(self):
        """
        Create the customer's full name if both first and last names are available.

        Returns:
            str: The full name "First, Last" if both names are present; otherwise, None.
        """

        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return None

    @property
    def recipient_name(self):
        """
        Provides the appropriate recipient name for addressing the customer in emails.

        Returns:
            str: First name if available or company name as a fallback.

        Raises:
            ValueError: If a name could not be created.
        """
        try:
            if self.first_name:
                return self.first_name

            return self.company

        except ValueError:
            raise ValueError(
                f"Recipient name could not be determined. Please ensure {self.email} has either a 'First Name' or 'Company' available"
            )

    def _parse_date(self, date_str):
        """
        Parses a string date into a datetime.date object.

        Parameters:
            date_str (str): Date in "YYYY-MM-DD" format.

        Returns:
            datetime.date: Parsed date, or None.
        """

        if date_str:
            try:
                return datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                print(
                    f"Warning: Invalid date format for customer {self.name}: {date_str}"
                )
        return None
