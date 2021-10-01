import sqlite3
from sqlite3 import Error
import db


def db_connection(db):
    connection = None
    try:
        connection = sqlite3.connect(db)
        print("Database connection established.")
        return connection
    except Error as e:
        print("Error: ", e)
    return connection


def main():
    con = db_connection(r"sqlite/db/database.db")
    row = '145', 'Cork', 'Van', '2 days'
    db.insert_row(con, 'bookings', row)


if __name__ == '__main__':
    main()
