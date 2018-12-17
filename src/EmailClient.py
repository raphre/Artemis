import imaplib
from email import message_from_string

MAGIC_CODE = '(RFC822)'

class EmailClient:
    def __init__(self, user):
        self.mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        self.user = user

    def login(self, username, password):
        self.mail.login(username, password)

    def _get_from_codes(self):
        status, data = self.mail.search(None, 'FROM', self.user)
        if status == 'OK':
            return data[0].split()

    def _get_unseen_codes(self):
        status, data = self.mail.search(None, 'UNSEEN')
        if status == 'OK':
            return data[0].split()

    def _get_fom_unseen_codes(self):
        self.mail.select('INBOX')
        from_codes = self.get_from_codes()
        unseen_codes = self.get_unseen_codes()
        return = list(set(from_codes) & set(unseen_codes))

    def _fetch_raw_message(self, code):
        status, data = self.mail.fetch(code, MAGIC_CODE)
        if status == 'OK':
            return data[0]

    def _process_raw_message(self, raw_message):
        msg = email.message_from_string(raw_message)
        subject = msg['Subject']
        if msg.is_multipart():
            body = msg.get_payload()[0].get_payload()
        else:
            body =  msg.get_payload()
        return (subject, body)

    def get_new_messages(self):
        from_unseen_codes = self._get_unseen_codes(self)
        messages = []
        for code in from_unseen_codes:
            raw_message = self._fetch_raw_message(code)
            message = self._process_raw_message(raw_message)
            messages.append(message)
        return messages

    def close(self):
        self.mail.close()
