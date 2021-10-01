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
            sql = "INSERT INTO " + table + "(userId,city,vehicleType, length) VALUES(?,?,?,?) "

        ex = con.cursor()
        ex.execute(sql, row)
        con.commit()
        print("Row inserted")
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
                        length text NOT NULL
                        );"""

    con = db_connection(r"sqlite/db/database.db")
    create_table(con, location_table)
    create_table(con, booking_table)

    row = ('cork', 'Cork', 'University College Cork, Cork City')
    insert_row(con, "locations", row)


if __name__ == '__main__':
    main()
