import sqlite3
from sqlite3 import Error


def db_connection(db):
    connection = None
    try:
        connection = sqlite3.connect(db)
        print("Database connection established.")
        return connection
    except Error as e:
        print("Error: ", e)
    return connection


def create_table(con, table_sql):
    try:
        connection = con.cursor()
        connection.execute(table_sql)
        print("Table created.")
    except Error as e:
        print("Error: ", e)


def insert_row(con, table, row):
    try:
        if 'locations' in table:
            sql = "INSERT INTO " + table + "(id,city,address) VALUES(?,?,?) "
        elif 'bookings' in table:
            sql = "INSERT INTO " + table + "(userId,city,vehicleType, startDate, endDate) VALUES(?,?,?,?,?) "
        elif 'users' in table:
            sql = "INSERT INTO " + table + "(username, firstName, lastName, email, phoneNumber, salt, hashedPassword) VALUES(?,?,?,?,?,?,?)"

        ex = con.cursor()
        ex.execute(sql, row)
        con.commit()
        print("Row inserted")
        return ex.lastrowid
    except Error as e:
        print("Error: ", e)


"""def remove_row(con, table, row):
    try:
        if 'locations' in table:
            pass
        elif 'bookings' in table:
            pass

        ex = con.cursor()
        ex.execute(sql, row)
        con.commit()
        print("Row removed")
        return ex.lastrowid
    except Error as e:
        print("Error: ", e)"""


def update_row(con, table, row):
    try:
        if 'locations' in table:
            pass
        elif 'bookings' in table:
            sql = "UPDATE " + table + " SET city = ?, vechicleType = ?, startDate = ?, endDate = ? WHERE userId = ?"

        ex = con.cursor()
        ex.execute(sql, row)
        con.commit()
        print("Row updated")
        return ex.lastrowid
    except Error as e:
        print("Error: ", e)

def main():
    location_table = """CREATE TABLE IF NOT EXISTS locations (
                        id text PRIMARY KEY,
                        city text,
                        address text NOT NULL
                        );"""

    booking_table = """CREATE TABLE IF NOT EXISTS bookings (
                        userId integer PRIMARY KEY,
                        city text NOT NULL,
                        vehicleType text NOT NULL,
                        startDate text NOT NULL,
                        endDate text NOT NULL
                        );"""

    users_table = """CREATE TABLE IF NOT EXISTS users (
                        userId integer PRIMARY KEY AUTOINCREMENT,
                        username text NOT NULL,
                        firstName text NOT NULL,
                        lastName text,
                        email text NOT NULL,
                        phoneNumber text,
                        salt text NOT NULL,
                        hashedPassword text NOT NULL
                        );"""

    con = db_connection(r"sqlite/db/database.db")
    create_table(con, location_table)
    create_table(con, booking_table)
    create_table(con, users_table)

    row = ('cork', 'Cork', 'University College Cork, Cork City')
    insert_row(con, "locations", row)

if __name__ == '__main__':
    main()
