import os
from os import path
from pathlib import PurePath
from InfoGetter import InfoGetter
from User import User

def create_new_user(credentials_path, password):
    getter = InfoGetter()
    items = ['email address', 'email password', 'blackboard username', 'blackboard password']
    credentials = getter.get_info_for(items)
    user = User(password)
    bb_creds = {}
    bb_creds['username'] = credentials['blackboard username']
    bb_creds['password'] = credentials['blackboard password']
    email_creds = {}
    email_creds['username'] = credentials['email address']
    email_creds['password'] = credentials['email password']
    user.create(credentials_path, bb_creds, email_creds)

def initial_setup(credentials_path, password):
    print('No users found.')
    print('Running initial setup ... ')
    user_path = credentials_path / '0'
    os.makedirs(user_path.as_posix())
    print('The directories have been made for the first user.')
    create_new_user(user_path, password)
