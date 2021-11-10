import sqlite3
from sqlite3 import Error


class Colour:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class DataCheck:
    def __init__(self, table, data):
        self.table = table
        self.data = data

    def users_check(self):
        conn = sqlite3.connect(r"C:\Users\damla\PycharmProjects\Car-Rental-System\sqlite\db\database.db")
        cursor = conn.cursor()
        print(self.data["username"])
        cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?",
                       (self.data["username"], self.data["email"]))
        if cursor.fetchone() is not None:
            raise Exception("User already exists")


class RegisterHandler:
    def __init__(self, table, data, salt, password):
        self.table = table
        self.data = data
        self.salt = salt
        self.password = password

    def perform_register(self):
        try:
            conn = sqlite3.connect(r"C:\Users\damla\PycharmProjects\Car-Rental-System\sqlite\db\database.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO 'users' (username, firstName, lastName, email, phoneNumber, points, salt, "
                "hashedPassword) VALUES(?,?,?,?,?,?,?,?)",
                (self.data["username"], self.data["firstname"], self.data["lastname"], self.data["email"],
                 self.data["phone"], 0, self.salt, self.password))
            conn.commit()

        except (Exception, Error) as e:
            print(Colour.RED + Colour.BOLD + "ERROR: " + str(e) + Colour.END)
            return e
