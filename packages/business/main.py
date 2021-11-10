import hashlib
import hmac
import os
from typing import Tuple

import packages.database.db as db
import packages.business.globalVariables as gV


# adapted from Mark Amery - https://stackoverflow.com/a/56915300
def hash_password(password: str) -> Tuple[bytes, bytes]:
    salt = os.urandom(16)
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 1000000)
    return salt, password_hash


def check_password(salt: bytes, password_hash: bytes, password: str) -> bool:
    return hmac.compare_digest(
        password_hash,
        hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 1000000)
    )


class Register:
    def __init__(self, table, data):
        self.table = table
        self.data = data

    def init_register(self):
        try:
            assert type(self.data) is dict
            try:
                db.DataCheck('users', self.data).users_check()
            except Exception as e:
                print(e)
                raise Exception("User already exists2")
            # user does not already exist
            salt, password = hash_password(self.data["password"])
            db.RegisterHandler('users', self.data, salt, password).perform_register()

        except AssertionError as e:
            return e

    def register_cleanup(self):
        gV.RUSERNAME.set("")
        gV.FIRSTNAME.set("")
        gV.LASTNAME.set("")
        gV.EMAIL.set("")
        gV.PHONENUMBER.set("")
        gV.RPASSWORD.set("")
        self.data = {}


class Login:
    def __init__(self, table, data):
        self.table = table
        self.data = data

    def init_login(self):
        try:
            assert type(self.data) is dict
            try:
                db.DataCheck('users', self.data).login_check()
            except Exception as e:
                print(e)
                raise Exception("User does not exist")
            # user does exist
          db.LoginHandler('user', self.data)


        except AssertionError as e:
            return e

    def login_cleanup(self):
        gV.USERNAME.get()
        gV.PASSWORD.get()
        self.logindata = {}

