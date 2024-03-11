# pymail2file

This is a Python package that allows you to save email attachments to a file, on specific folder according to rules/filters.

You can save the files to:
- Local storage
- GDrive

## Example [tests.py](tests.py)

### Create your .env file, e.g.
```
IMAP_HOST=mail.infomaniak.com
IMAP_PORT=993
SMPT_HOST=mail.infomaniak.com
SMTP_PORT=465
EMAIL_USER=SUPEREMAIL@etik.com
EMAIL_PASSWORD="SUPERPASSWORD"
ADMIN_EMAIL=MYADMINACCOUNT@ik.me
```

## Prepare your GDrive Account
If you want to use the GDrive part of the example, follow this part on [PyDrive2](https://docs.iterative.ai/PyDrive2/quickstart/#authentication): 
- Create the application on your [Google APIs Console](https://console.cloud.google.com/iam-admin/projects) and save the JSON in `client_secrets.json`

- Run the `tests.py`, the first time, a web page will open, accept the connection between the application you created and your Google Account ; a file `credentials.json` will be created, you will not need to log in next time.
