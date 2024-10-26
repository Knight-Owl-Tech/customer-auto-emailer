# Email Automation Tool

### Overview

This project is an **automated email follow-up system** designed to streamline communication with customers for small businesses. Using Python and the `smtplib` library, the tool automates sending follow-up emails based on customer data stored in a shared Google Sheets spreadsheet.

The goal is to simplify customer management and improve engagement by ensuring timely and personalized follow-up emails after interactions, such as sales or support requests.

### Features

- **Automated Email Sending**: Schedule and send follow-up emails based on specific time intervals.
- **Google Sheets Integration**: Fetch customer information directly from a shared Google Sheets spreadsheet.
- **Customizable Email Templates**: Use or modify email templates to suit your business communication style.

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

     - Google Spreadsheet ID

       - The Google Sheets ID is the long string of characters in the URL when you open the Google Sheet. For example, in a URL like https://docs.google.com/spreadsheets/d/some-extremely-long-hash/edit, the ID is some-extremely-long-hash.

     - Your email address to use

     - Follow-Up interval that represents number of days

   ```config
   [google_sheets]
   spreadsheet_id = your-spreadsheet-id

   [smtp_settings]
   email_address = your-email@gmail.com

   [email_automation]
   default_follow_up_interval = some_int_value
   ```

### File Structure

```bash
├── README.md
├── pyproject.toml
├── email_automation.py # Main script for automating email follow-ups
├── config.py # Email credentials and configuration
├── google_sheets.py # Script to interact with Google Sheets
├── templates/ # Folder for email templates
│   ├── formal_follow-up.html   # Template for Formal email style
│   └── casual_follow-up.html   # Template for Casual email style
├── email.cfg # File to contain important info (not included in repo)
└── credentials.json # Google Sheets Service Account credentials (not included in repo)
```

### Usage

1. **Populate the Google Sheet**:

   - To set up the Google Sheets template, [click here](https://docs.google.com/spreadsheets/d/19aBWnh2iwkLwcHIX3nVqzdvzlZaCTQP5I4vXTaQi-M4/copy) to make a copy of the template in your own Google Drive. After making a copy, share the new sheet with your Google Service Account email to allow your project to access it.

   - Below gives a description of each column:

   | Column Name                   | Cell Type                  | Description                                             |
   | ----------------------------- | -------------------------- | ------------------------------------------------------- |
   | **Name**                      | Google ‘People’ Smart Chip | Links to Google Contacts                                |
   | **firstName**                 | Text (protected)           | Auto-generated based on "Name"                          |
   | **lastName**                  | Text (protected)           | Auto-generated based on "Name"                          |
   | **Email**                     | Text                       | Manual entry for customer email                         |
   | **Follow-Up?**                | Checkbox                   | Boolean value: True (checked) or False (unchecked)      |
   | **Email Style**               | Dropdown (text)            | Choose between styles: "Formal" or "Casual"             |
   | **Custom Follow-Up Interval** | Number                     | Optional, custom interval for follow-ups per customer   |
   | **Notes**                     | Text                       | Additional notes about the customer                     |
   | **Last Contact Date**         | Date (protected)           | Auto-updated by script to track last email contact date |

2. **Run the script**:

   ```python
   python email_automation.py
   ```

   - The script will check for customers due for follow-up emails and send them based on their designated email style and follow-up interval. After a successful email, the "Last Contact Date" column is updated automatically.

### Customization

- Email Templates: Modify the HTML templates in the `templates/` directory to match your business's tone and branding.

- Scheduling: Adjust the follow-up intervals or email content in the email_automation.py file to meet your needs.

### Troubleshooting

- SMTP Authentication: Make sure you've enabled "Less Secure Apps" or created an App Password if using 2-Factor Authentication (2FA) on your Google account.

- Google Sheets API: Ensure that the Google Sheet is shared with the Service Account email associated with the credentials.json file.

### Future Improvements

- **Enhanced error logging**: Improve logging for better insights into failed attempts and errors.
- **Support for multiple email providers**: Expand beyond Gmail to allow compatibility with other email services.
