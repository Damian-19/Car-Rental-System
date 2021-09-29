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


def insert_dummy_location_data(con, row):
    try:
        sql = """INSERT INTO locations(id,city,address) VALUES(?,?,?) """

        ex = con.cursor()
        ex.execute(sql, row)
        con.commit()
        return ex.lastrowid
        print("Data inserted.")
    except Error as e:
        print("Error: ", e)


def main():
    location_table = """CREATE TABLE IF NOT EXISTS locations (
                        id text PRIMARY KEY,
                        city text,
                        address text NOT NULL
                        );"""

    con = db_connection(r"sqlite/db/database.db")
    create_table(con, location_table)

    row = ('lim', 'Limerick', 'University of Limerick, Castletroy, Limerick')
    insert_dummy_location_data(con, row)


if __name__ == '__main__':
    main()
