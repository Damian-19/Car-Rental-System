import sqlite3
from sqlite3 import Error

from packages.business import globalVariables as gv
from packages.business import main as main


def get_userid():
    """
    Retrieves user ID from global variables
    """
    con = sqlite3.connect(r"../../sqlite/db/database.db")
    cursor = con.cursor()
    try:
        cursor.execute("SELECT userId FROM users WHERE username = ?", (str(gv.USERNAME.get()),))
        return str(cursor.fetchone()[0])
    except Error as e:
        print(f"{Colour.RED} {Colour.BOLD} GET USERID ERROR: {str(e)} {Colour.END}")


class DatabaseHandler:
    """
    Class to perform database operations
    """
    def __init__(self, table, data):
        self.table = table
        self.data = data

    def check_bookings(self):
        """
        Retrieves number of bookings for user
        Currently Unused
        """
        con = sqlite3.connect(r"../../sqlite/db/database.db")
        cursor = con.cursor()
        try:
            if 'bookings' in self.table:
                cursor.execute("SELECT * FROM " + self.table + " WHERE userId = ?", (self.data["userid"]))
                i = 0
                while cursor.fetchall():
                    i += 1
                print(f"{i} row(s) found")
                return i
            else:
                raise Exception('incorrect table')

        except Error as e:
            print(f"{Colour.RED} {Colour.BOLD} BOOKINGS CHECK ERROR: {str(e)} {Colour.END}")

    def retrieve_booking(self):
        """
        Checks for bookings for user
        """
        con = sqlite3.connect(r"../../sqlite/db/database.db")
        cursor = con.cursor()
        try:
            if 'bookings' in self.table:
                cursor.execute("SELECT startDate, endDate FROM " + self.table + " WHERE userId = ?",
                               (self.data["userid"]))
                if cursor.fetchall() is not None:
                    return cursor.fetchall()
            else:
                raise Exception("No bookings found")
        except Error as e:
            print(f"{Colour.RED} {Colour.BOLD} BOOKINGS RETRIEVE ERROR: {str(e)} {Colour.END}")

    def retrieve_user_points(self):
        """
        Returns users points from database
        """
        con = sqlite3.connect(r"../../sqlite/db/database.db")
        cursor = con.cursor()
        try:
            if 'users' in self.table:
                cursor.execute("SELECT points FROM " + self.table + " WHERE userId = ?", (self.data["userid"]))
                return str(cursor.fetchone()[0])
            else:
                raise Exception("No user / points found")
        except Error as e:
            print(f"{Colour.RED} {Colour.BOLD} POINTS RETRIEVE ERROR: {str(e)} {Colour.END}")

    def add_booking(self):
        """
        Adds an entry into the booking table
        """
        try:
            con = sqlite3.connect(r"../../sqlite/db/database.db")
            cursor = con.cursor()

            cursor.execute("INSERT INTO bookings (userId,city,vehicleType, startDate, endDate) VALUES(?,?,?,?,?) ",
                           (self.data["userid"], self.data["location"], self.data["vehicle"], self.data["startdate"],
                            self.data["enddate"]))
            con.commit()

        except Error as e:
            print(f"{Colour.RED} {Colour.BOLD} BOOKINGS CHECK ERROR: {str(e)} {Colour.END}")

        print("add_booking finished")

    def update_user_points(self):
        """
        Updates the users points in the database
        """
        con = sqlite3.connect(r"../../sqlite/db/database.db")
        cursor = con.cursor()
        try:
            cursor.execute("UPDATE users SET points = ? WHERE userId = ?", (self.data["points"], self.data["userid"]))
            con.commit()
            print(f"{Colour.GREEN} {Colour.BOLD} Points update successful. {Colour.END}")
        except Error as e:
            print(f"{Colour.RED} {Colour.BOLD} POINTS UPDATE ERROR: {str(e)} {Colour.END}")


class DataCheck:
    """
    Performs comparisons on database tables
    """
    def __init__(self, table, data):
        self.table = table
        self.data = data

    def users_check(self):
        """
        Checks if a user already exists in the database
        """
        conn = sqlite3.connect(r"../../sqlite/db/database.db")
        cursor = conn.cursor()
        print(self.data["username"])
        cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?",
                       (self.data["username"], self.data["email"]))
        if cursor.fetchone() is not None:
            raise Exception("User already exists")

    def login_check(self):
        """
        Performs the login, compares user-provided password and username with those stored in the database
        """
        conn = sqlite3.connect(r"..\..\sqlite\db\database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT salt, hashedPassword FROM users WHERE username = ?",
                       ([self.data["username"]]))
        # if cursor.fetchall() is None:
        # raise Exception("User does not exist in database")
        salt, password = cursor.fetchone()
        assert main.check_password(salt, password, self.data["password"])


class RegisterHandler:
    """
    Handles registering a user into the database
    MVC - Controller
    """
    def __init__(self, table, data, salt, password):
        self.table = table
        self.data = data
        self.salt = salt
        self.password = password

    def perform_register(self):
        """
        Attempts to insert user data into database table
        """
        try:
            conn = sqlite3.connect(r"../../sqlite/db/database.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO 'users' (username, firstName, lastName, email, phoneNumber, points, salt, "
                "hashedPassword) VALUES(?,?,?,?,?,?,?,?)",
                (self.data["username"], self.data["firstname"], self.data["lastname"], self.data["email"],
                 self.data["phone"], 0, self.salt, self.password))
            conn.commit()

        except (Exception, Error) as e:
            # print(Colour.RED + Colour.BOLD + "ERROR: " + str(e) + Colour.END)
            print(f"{Colour.RED} {Colour.BOLD} ERROR: {str(e)} {Colour.END}")
            return e


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
