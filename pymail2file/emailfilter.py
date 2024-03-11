# https://pypi.org/project/imap-tools/
# https://stackoverflow.com/questions/882712/send-html-emails-with-python
from imap_tools import MailBox, AND, MailMessageFlags, MailMessage
import os
from email.message import EmailMessage
from smtplib import SMTP_SSL, SMTP_SSL_PORT

from . import GDrive

class EmailFilter:
    _email_user = ""
    _email_pass = ""
    _imap_host = ""
    _imap_port = ""
    _admin_email = ""
    _main_folder = ""
    _email_filters = None
    _smtp_host = ""
    _smtp_port = ""
    _gdrive = None
    _send_email = False

    _mailbox = None

    def __init__(self, email_user: str, email_pass: str, imap_host: str, imap_port: int, admin_email: str, main_folder: str, email_filters: dict, smtp_host: str=None, smtp_port: int=None, gdrive: bool=False, send_email: bool=False):
        self._email_user = email_user
        self._email_pass = email_pass
        self._imap_host = imap_host
        self._imap_port = imap_port
        self._admin_email = admin_email
        self._main_folder = main_folder
        self._email_filters = email_filters
        self._smtp_host = smtp_host
        self._smtp_port = smtp_port
        self._send_email = send_email

        if gdrive:
            self._gdrive = GDrive(self._main_folder)
        else :
            self._gdrive = None

        self._mailbox = MailBox(self._imap_host,self._imap_port).login(self._email_user, self._email_pass)
        
    def get_matching_filters(self, msg: MailMessage) -> list:
        matching_filters = []
        for filter in self._email_filters:
            test = False
            if msg.from_values.email in filter["from"]:
                for subject in filter["tests"]["subject_contains"]:
                    if subject in msg.subject.lower():
                        test = True
                        pass
                if test:
                    for att in msg.attachments:
                        if att.content_type in filter["tests"]["content_type"]:
                            matching_filters.append(filter)    
        return matching_filters

    def send_email(self, to: str, subject: str, body: str):
        if (self._send_email):
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = self._email_user
            msg['To'] = to
            msg.set_content(body, subtype='plain')
            with SMTP_SSL(self._smtp_host, self._smtp_port) as s:
                s.login(self._email_user, self._email_pass)
                s.send_message(msg)

    def save_file(self, folder_path: str, filename: str, payload: bytes, content_type: str):
        if self._gdrive is not None:
            self._gdrive.upload_file_to_folder(folder_path, filename, payload, content_type)
        else:
            if not os.path.exists(folder_path): 
                os.makedirs(folder_path) 
            filePath = os.path.join(folder_path, filename)
            if not os.path.isfile(filePath) :
                fp = open(filePath, 'wb')
                fp.write(payload)
                fp.close()

    def run(self):
        for msg in self._mailbox.fetch(AND(seen=False)):
            #print(msg.date, msg.from_values, msg.to_values, msg.subject, len(msg.text or msg.html), msg.uid)
            self._mailbox.flag(msg.uid, (MailMessageFlags.SEEN, MailMessageFlags.FLAGGED), False)

            mathing_filters = self.get_matching_filters(msg)
            # Error, more than one rule match
            if (len(mathing_filters) > 1):
                print("Error, more than one rule match")
                # Mark email as FLAGGED and UNSEEN
                self._mailbox.flag(msg.uid, (MailMessageFlags.FLAGGED), True)
                self._mailbox.flag(msg.uid, (MailMessageFlags.SEEN), True)

                # Send email to admin
                self.send_email(self._admin_email, "Error, more than one rule match", "Message received "+ str(msg.date) +" from " + msg.from_values.email + " with subject \"" + msg.subject + "\" has more than one rule match. Please check the rules.")


            elif (len(mathing_filters) == 0):
                print("Error, no rule match")
                # Mark email as FLAGGED and UNSEEN
                self._mailbox.flag(msg.uid, (MailMessageFlags.FLAGGED), True)
                self._mailbox.flag(msg.uid, (MailMessageFlags.SEEN), True)
                
                # Send email to admin
                self.send_email(self._admin_email, "Error, no rule match", "Message received " + str(msg.date) +" from " + msg.from_values.email + " with subject \"" + msg.subject + "\" has no rule match. Please check the rules.")

            else:
                rule = mathing_filters[0]
                
                self._mailbox.flag(msg.uid, (MailMessageFlags.FLAGGED), False)
                self._mailbox.flag(msg.uid, (MailMessageFlags.SEEN), True)

                for att in msg.attachments:  # list: imap_tools.MailAttachment
                    if (att.content_type in rule["tests"]["content_type"]):
                        print(att.filename, att.content_type, att.size)
                        folder_path = self._main_folder + "/" + rule["destination"]
                        self.save_file(folder_path, att.filename, att.payload, att.content_type)