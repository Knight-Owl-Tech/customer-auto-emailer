# Email Automation Tool

### Overview

This project is an **automated email follow-up system** designed to streamline communication with customers for small businesses. Using Python and the `smtplib` library, the tool automates the sending of follow-up emails based on customer data stored in a shared Google Sheets spreadsheet.

The goal is to simplify customer management and improve engagement by ensuring timely and personalized follow-up emails after interactions, such as sales or support requests.

### Features

- **Automated Email Sending**: Schedule and send follow-up emails based on specific time intervals.
- **Google Sheets Integration**: Fetch customer information directly from a shared Google Sheets spreadsheet.
- **Customizable Email Templates**: Use or modify email templates to suit your business communication style.
- **Error Handling**: Basic error handling for failed email sends and incorrect data entries.

### Requirements

- A Google account with a shared Google Sheet containing customer data
- Access to the **Google Sheets API**
- A Google account set up for SMTP access (Google Workspace or regular Gmail)

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/KnightOwlTech/auto-emailer.git
   cd auto-emailer
   ```

2. **Set up the environment**:

   - Create a virtual environment and activate it:
     ```bash
     python3 -m venv venv
     source venv/bin/activate  # On Windows, use venv\Scripts\activate
     ```
   - Install the required Python libraries:
     ```bash
     pip install -r requirements.txt
     ```

3. **Set up Google Sheets API**:

   - Go to the [Google Developers Console](https://console.developers.google.com/), create a project, and enable the **Google Sheets API**.
   - Download your **credentials.json** file and place it in the project directory.
   - Follow the [Google Sheets API Python Quickstart](https://developers.google.com/sheets/api/quickstart/python) for more details.

4. **Configure your SMTP settings**:
   - Set up your Google account for SMTP access and generate an App Password if using 2FA.
   - Update the `config.py` file with your email credentials:
     ```python
     EMAIL_ADDRESS = 'your-email@gmail.com'
     EMAIL_PASSWORD = 'your-app-password'
     ```

### Usage

1. **Populate the Google Sheet**:

   - The Google Sheet should include columns for `Name`, `Email`, `Last Contact Date`, and `Follow-Up Interval`.

2. **Run the script**:

   ```bash
   python email_automation.py
   ```

3. **Scheduled Follow-Ups**:
   - The script will automatically check for customers who are due for follow-up emails and send them accordingly.

### File Structure

```
├── README.md
├── pyproject.toml
├── email_automation.py # Main script for automating email follow-ups
├── config.py # Email credentials and configuration
├── google_sheets.py # Script to interact with Google Sheets
├── templates/ # Folder for email templates
│ |-- followup_template_1.html
│ └── followup_template_2.html
└── credentials.json # Google Sheets API credentials (not included in repo)
```

### Customization

- **Email Templates**: Modify the HTML templates in the `templates/` directory to match your business's tone and branding.
- **Scheduling**: Adjust the follow-up intervals or email content in the `email_automation.py` file to meet your needs.

### Troubleshooting

- **SMTP Authentication**: Make sure you've enabled "Less Secure Apps" or created an App Password if using 2-Factor Authentication (2FA) on your Google account.
- **Google Sheets API**: Ensure the correct API credentials are in place, and that the Google Sheets file is shared with the account linked to your credentials.

### Future Improvements

- Integration with additional CRM tools for more robust customer tracking.
- Support for multiple email providers.
- Improved error logging and notifications.
