from pymail2file import EmailFilter
import os
from dotenv import load_dotenv
load_dotenv()

email_user = os.getenv('EMAIL_USER')
email_pass = os.getenv('EMAIL_PASSWORD')
imap_host = os.getenv('IMAP_HOST')
imap_port = os.getenv('IMAP_PORT')
smtp_host = os.getenv('SMTP_HOST')
smtp_port = os.getenv('SMTP_PORT')
admin_email = os.getenv('ADMIN_EMAIL')

# For GDrive
gdrive = False
if gdrive:
    main_folder = "Mail2File/Tests"
else :
    main_folder = "./build"

filters = [
    {
        "rule_name": "Rule1",
        "from": ["tests@gmail.com"],
        "tests": {
            "subject_contains": ["test1"],
            "content_type": ["application/pdf"]
        },
        "destination": "folder_rule1"
    }, 
    {
        "rule_name": "Rule2",
        "from": ["myemail@gmail.com", "tests@etik.com"],
        "tests": {
            "subject_contains": ["simple"],
            "content_type": ["application/pdf"]
        },
        "destination": "folder_rule2"
    }
]

mailFilter = EmailFilter(email_user, email_pass, imap_host, imap_port, admin_email, main_folder, filters, smtp_host, smtp_port, gdrive)
mailFilter.run()