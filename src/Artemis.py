from User import User
from Aux import *
from InfoGetter import InfoGetter
from pathlib import PurePath
import os

class Artemis:
    def __init__(self, password):
        root_path = PurePath(os.path.realpath(__file__)).parents[1]
        self.credentials_path = root_path / 'credentials'
        if not os.path.isdir(self.credentials_path.as_posix()):
            initial_setup(self.credentials_path, password)
        user_dirs = os.listdir(self.credentials_path.as_posix())
        user_dirs = list(filter(lambda dir: dir.isdigit(), user_dirs))
        user_paths = [root_path / 'credentials' / PurePath(path) for path in user_dirs]
        self.users = []
        for path in user_paths:
            user = User(password)
            user.load_from(path)
            self.users.append(user)

    def run(self):
        print('Cheecking for requests...')
        self.users[0].process_requests()
