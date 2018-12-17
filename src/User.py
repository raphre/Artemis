from os import path
from KeyChain import KeyChain
import imaplib
from WebDriver import WebDriver, Course
from pathlib import PurePath
from EmailClient import EmailClient

class User:
    def __init__(self, password):
        """
        Just reserves the variables and puts the user in a state of being logged out.
        """
        self.path_to_credentials = None
        self.logged_in_to_email = False
        self.logged_in_to_bb = False
        self.web_driver = None
        self.bb_username = None
        self.key_chain = None
        self.password = password

    def create(self, path_to_credentials, bb_creds, mail_creds):
        """
        Records the user with the given credentials as a new user.
        """
        self.path_to_credentials = path_to_credentials
        bb_name = bb_creds['username']
        bb_pass = bb_creds['password']
        mail_name = mail_creds['username']
        mail_pass = mail_creds['password']
        self.key_chain = KeyChain(self.path_to_credentials, self.password)
        self.key_chain.update_credentials_for('bb', bb_name, bb_pass)
        self.key_chain.update_credentials_for('mail', mail_name, mail_pass)

    def load_from(self, path_to_credentials):
        """
        Loads the user from their credentials path.
        """
        self.path_to_credentials = path_to_credentials
        self.key_chain = KeyChain(self.path_to_credentials, self.password)
        self.mail = EmailClient('raphre')

    def login_to(self, service):
        """
        Sets the user into a state of being logged in to the given service.
        """
        if (service == 'mail'):
            if (self.logged_in_to_email == True):
                print('User is already logged in to email.')
                return
            else:
                self.mail = imaplib.IMAP4_SSL(SMTP_SERVER)
                username, password = self.key_chain.get_credentials_for('mail')
                self.mail.login(username, password)
                self.logged_in_to_email = True
                return
        if (service == 'bb'):
            if (self.logged_in_to_bb == True):
                print('User is already logged into B.B.')
                return
            else:
                self.web_driver = WebDriver()
                username, password = self.key_chain.get_credentials_for('bb')
                self.web_driver.login(username, password)
                self.logged_in_to_bb = True
                return

    def create_announcement(self, subject, announcement, course):
        if not self.logged_in_to_bb:
            self.login_to('bb')
        self.web_driver.enter_course(course)
        self.web_driver.create_announcement(subject, announcement)
        print('Posted an announcement!')

    def process_requests(self):
        if not self.logged_in_to_email:
            self.login_to('mail')
        batch = self.mail.get_new_messages()
        for subject, message in batch:
            self.create_announcement(subject, message, 'MAT 105.02')

    def logout(self):
        if self.logged_in_to_bb:
            self.web_driver.quit()
