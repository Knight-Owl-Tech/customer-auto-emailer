# Email Automation Tool

### Overview

This project is an **automated email follow-up system** designed to streamline communication with customers for small businesses. Using Python and the `smtplib` library, the tool automates sending follow-up emails based on customer data stored in a shared Google Sheets spreadsheet.

The goal is to simplify customer management and improve engagement by ensuring timely and personalized follow-up emails after interactions, such as sales or support requests.

### Features

- **Automated Email Sending**: Schedule and send follow-up emails based on specific time intervals.
- **Google Sheets Integration**: Fetch customer information directly from a shared Google Sheets spreadsheet.
- **Customizable Email Templates**: Use or modify email templates to suit your business communication style.
- **Error Handling**: Basic error handling for failed email sends and incorrect data entries.

### Requirements

- Access to the **Google Sheets API** via a Google Service Account
- A Google account set up for SMTP access (Google Workspace or regular Gmail)

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/KnightOwlTech/customer-auto-emailer.git
   cd auto-emailer
   ```

2. **Set up the environment**:

   - Create a virtual environment and activate it:

     for macOS

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

     for Windows

     ```bash
     python3 -m venv venv
     source venv/Scripts/activate
     ```

   - Install the required dependencies using `pyproject.toml`:

     ```bash
     pip install .
     ```

3. **Set up Google Sheets API with a Service Account**:

   - Go to the [Google Developers Console](https://console.cloud.google.com), create a project, and enable the Google Sheets API.

   - Create a Service Account within your project. You will also need to create a new key.

   - Download the credentials.json file for your Service Account and place it in the project directory.

   - Share your Google Sheet with the Service Account email (e.g., your-service-account@your-project.iam.gserviceaccount.com) so it has permission to read data. If your project requires "write" then select "Editor"

4. **Configure your SMTP settings**:

   - Set up your Google account for SMTP access and generate an App Password if using 2FA.

   - You will need to include an `email.cfg` file at the root project directory and store the following information.

     - The Google Sheets ID is the long string of characters in the URL when you open the Google Sheet. For example, in a URL like https://docs.google.com/spreadsheets/d/some-extremely-long-hash/edit, the ID is some-extremely-long-hash.

   ```config
   [google_sheets]
   spreadsheet_id = your-spreadsheet-id

   [smtp_settings]
   email_address = 'your-email@gmail.com'
   ```

### File Structure

```bash
├── README.md
├── pyproject.toml
├── email_automation.py # Main script for automating email follow-ups
├── config.py # Email credentials and configuration
├── google_sheets.py # Script to interact with Google Sheets
├── templates/ # Folder for email templates
│   ├── followup_template_1.html # you create your templates as necessary (not included in repo)
│   └── followup_template_2.html
├── email.cfg # File to contain important info (not included in repo)
└── credentials.json # Google Sheets Service Account credentials (not included in repo)
```

### Usage

1. **Populate the Google Sheet**:

   - The Google Sheet should include columns for Name, Email, Last Contact Date, and Follow-Up Interval.

2. **Run the script**:

   ```python
   python email_automation.py
   ```

3. **Scheduled Follow-Ups**:

   - The script will automatically check for customers who are due for follow-up emails and send them accordingly.

### Customization

- Email Templates: Modify the HTML templates in the `templates/` directory to match your business's tone and branding.

- Scheduling: Adjust the follow-up intervals or email content in the email_automation.py file to meet your needs.

### Troubleshooting

- SMTP Authentication: Make sure you've enabled "Less Secure Apps" or created an App Password if using 2-Factor Authentication (2FA) on your Google account.

- Google Sheets API: Ensure that the Google Sheet is shared with the Service Account email associated with the credentials.json file.

### Future Improvements

- Improved error logging and notifications.

- Support for multiple email providers.
