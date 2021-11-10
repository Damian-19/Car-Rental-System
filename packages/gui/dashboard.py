import sqlite3
import tkinter as tk
import tkinter.ttk as ttk
from packages.business import globalVariables as gv


def database():
    # create database connection
    global conn, cursor
    conn = sqlite3.connect(r"../../sqlite/db/database.db")
    cursor = conn.cursor()


def begin_edit(button_name, save_info_button):
    button_name.config(state='normal')
    save_info_button.config(state='normal')


def create_dashboard():
    tabs = ttk.Notebook(gv.home)

    catalog_frame = tk.Frame(tabs)
    gv.rent_frame = tk.Frame(tabs)
    locations_frame = tk.Frame(tabs)
    gv.account_frame = tk.Frame(tabs)

    catalog_frame.grid(column=0, row=0)
    gv.rent_frame.grid(column=1, row=0)
    locations_frame.grid(column=2, row=0)
    gv.account_frame.grid(column=3, row=0)

    tabs.add(catalog_frame, text="Catalog")
    tabs.add(gv.rent_frame, text="Rent Car")
    tabs.add(locations_frame, text="Locations")
    tabs.add(gv.account_frame, text="Account")

    tabs.grid(column=0, row=1)
    populate_account()


def populate_account():
    database()
    # first name
    cursor.execute("SELECT Firstname FROM users WHERE username = ? ", (gv.USERNAME.get(),))
    name = cursor.fetchone()
    name = str(name).replace("(", "").replace(")", "").replace("'", "").replace(",", "")

    first_name = tk.Label(gv.account_frame, text="First Name").grid(column=0, row=0, padx=5, pady=5)
    first_name = tk.Entry(gv.account_frame, text=name)
    first_name.insert(0, string=name)
    first_name.grid(column=1, row=0)
    first_name.config(state='readonly')

    save_button = tk.Button(gv.account_frame, text="Save")
    save_button.config(state='disabled')
    save_button.grid(column=3, row=0, columnspan=1, sticky="we", padx=5, pady=5)

    name_button = tk.Button(gv.account_frame, text="Edit", command=lambda: begin_edit(first_name, save_button))
    name_button.grid(column=2, row=0, columnspan=1, sticky="we", padx=5, pady=5)

    # last name
    cursor.execute("SELECT Lastname FROM users WHERE username = ? ", (gv.USERNAME.get(),))
    name = cursor.fetchone()
    name = str(name).replace("(", "").replace(")", "").replace("'", "").replace(",", "")

    last_name = tk.Label(gv.account_frame, text="Last Name").grid(column=0, row=1, padx=5, pady=5)
    last_name = tk.Entry(gv.account_frame, text=name)
    last_name.insert(0, string=name)
    last_name.grid(column=1, row=1)
    last_name.config(state='readonly')

    save_button1 = tk.Button(gv.account_frame, text="Save")
    save_button1.config(state='disabled')
    save_button1.grid(column=3, row=1, columnspan=1, sticky="we", padx=5, pady=5)

    name_button1 = tk.Button(gv.account_frame, text="Edit", command=lambda: begin_edit(last_name, save_button1))
    name_button1.grid(column=2, row=1, columnspan=1, sticky="we", padx=5, pady=5)
