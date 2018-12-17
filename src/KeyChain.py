import json, io, pyAesCrypt
from os import stat, remove, path
from pathlib import PurePath

class KeyChain:
    def __init__(self, path_to_credentials, password):
        self.path_to_credentials = path_to_credentials
        self.bufferSize = 64 * 1024
        self.password = password
        self.file_exists = path.isfile(self.path_to_credentials)

    def get_path_for(self, service):
        """
        Builds the path to the encrypted credentials file for the appropriate service.
        """
        path_extension = ""
        if service == "mail":
            path_extension="mail.json.aes"
        if service == "bb":
            path_extension="bb.json.aes"
        return self.path_to_credentials / path_extension

    def _decrypt_data(self, service):
        """
        Decrypts credentials data for the given service.
        """
        file_path = self.get_path_for(service)
        decrypted_stream = io.BytesIO()
        encrypted_size = stat(file_path).st_size
        with open(file_path, 'rb') as encrypted_file:
            pyAesCrypt.decryptStream(encrypted_file, decrypted_stream, self.password, self.bufferSize, encrypted_size)
            encrypted_file.close()
        decrypted_string = decrypted_stream.getvalue().decode('utf-8')
        data = json.loads(decrypted_string)
        return data

    def _encrypt_data(self, data, service):
        """
        Encrypts
        """
        file_path = self.get_path_for(service)
        data_to_encrypt = json.dumps(data).encode('utf-8')
        stream_to_encrypt = io.BytesIO(data_to_encrypt)
        with open(file_path, 'wb') as file:
            pyAesCrypt.encryptStream(stream_to_encrypt, file, self.password, self.bufferSize)
            file.close()

    def get_credentials_for(self, service):
        """
        Given a username in plaintext, returns the password in plaintext.
        """
        data = self._decrypt_data(service)
        username = data['username']
        password = data['password']
        return (username, password)

    def update_credentials_for(self, service, username, password):
        data = {}
        data['username'] = username
        data['password'] = password
        self._encrypt_data(data, service)
