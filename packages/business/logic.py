import hashlib
import hmac
import os
from datetime import datetime
from typing import Tuple

import packages.business.globalVariables as gV
import packages.database.db as db
from packages.business import errors


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


class BusinessLogic:
    def __init__(self, data):
        self.data = data
        self.startdate = self.data["startdate"]
        self.enddate = self.data["enddate"]

    def calculate_points(self):
        date_format = "%Y-%m-%d"
        date1 = datetime.strptime(str(self.startdate), date_format)
        date2 = datetime.strptime(str(self.enddate), date_format)
        delta = date2 - date1
        days = int(delta.days)
        days += 1

        database_points = db.DatabaseHandler('users', self.data).retrieve_user_points()
        # add points
        weeks = days / 7
        points = weeks * 25
        total_points = float(database_points) + points
        if total_points > 0:
            self.data["points"] = total_points

            db.DatabaseHandler('users', self.data).update_user_points()
        else:
            raise errors.NegativeDaysReached

        print(f"Points: {total_points}")
        print(f"Days: {days}")
        return total_points


class Register:
    """
    Performs the user register
    MVC - Controller
    """
    def __init__(self, table, data):
        self.table = table
        self.data = data

    def init_register(self):
        """
        Inserts user data into the database table
        """
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
        """
        Resets register form on GUI
        """
        gV.RUSERNAME.set("")
        gV.FIRSTNAME.set("")
        gV.LASTNAME.set("")
        gV.EMAIL.set("")
        gV.PHONENUMBER.set("")
        gV.RPASSWORD.set("")
        self.data = {}


class Login:
    """
    Performs the login
    MVC - Controller
    """
    def __init__(self, table, data):
        self.table = table
        self.data = data

    def init_login(self):
        """
        Performs the login user check and returns the result
        """
        try:
            assert type(self.data) is dict
            try:
                db.DataCheck('users', self.data).login_check()
            except Exception as e:
                print(e)
                raise Exception("User does not exist")

        except AssertionError as e:
            return e

    def login_cleanup(self):
        gV.USERNAME.get()
        gV.PASSWORD.get()
        self.data = {}
