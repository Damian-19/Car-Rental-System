import sqlite3
import tkinter as tk
import tkinter.ttk as ttk
from tkcalendar import Calendar, DateEntry
from packages.business import globalVariables as gv
from packages.database import db
from packages.business import  errors


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

    gv.booking_frame = tk.Frame(tabs)
    gv.rent_frame = tk.Frame(tabs)
    locations_frame = tk.Frame(tabs)
    gv.account_frame = tk.Frame(tabs)

    gv.booking_frame.grid(column=0, row=0)
    gv.rent_frame.grid(column=1, row=0)
    locations_frame.grid(column=2, row=0)
    gv.account_frame.grid(column=3, row=0)

    tabs.add(gv.booking_frame, text="Bookings")
    tabs.add(gv.rent_frame, text="Rent Car")
    tabs.add(locations_frame, text="Locations")
    tabs.add(gv.account_frame, text="Account")

    tabs.grid(column=0, row=1)
    populate_account()
    rent_tab()
    bookings_tab()


def bookings_tab():
    con = sqlite3.connect(r"../../sqlite/db/database.db")
    cursor = con.cursor()
    cursor.execute("SELECT city, vehicleType, startDate, endDate FROM bookings WHERE userid = ?", (db.get_userid(),))
    i = 1
    tk.Label(gv.booking_frame, text="Location").grid(row=0, column=0)
    tk.Label(gv.booking_frame, text="Vehicle Type").grid(row=0, column=1)
    tk.Label(gv.booking_frame, text="Rent Date").grid(row=0, column=2)
    tk.Label(gv.booking_frame, text="Return Date").grid(row=0, column=3)

    for e in cursor.fetchall():
        for j in range(len(e)):
            box = tk.Entry(gv.booking_frame, justify='center')
            box.grid(row=i, column=j)
            box.insert(tk.END, e[j])


def rent_tab():
    gv.rent_data = {}
    a = tk.Label(gv.rent_frame, text="Location").grid(row=0, column=0)
    b = tk.Label(gv.rent_frame, text="Vehicle Type").grid(row=1, column=0)
    c = tk.Label(gv.rent_frame, text="Start Date").grid(row=2, column=0)
    d = tk.Label(gv.rent_frame, text="End Date").grid(row=3, column=0)

    # location dropdown
    selected_location = tk.StringVar()
    location_dropdown = ttk.Combobox(gv.rent_frame, textvariable=selected_location)
    location_dropdown['values'] = ('Cork',
                                   'Limerick',
                                   'Dublin',
                                   'Waterford')
    location_dropdown['state'] = 'readonly'
    location_dropdown.grid(row=0, column=1)

    # vehicle dropdown
    selected_vehicle = tk.StringVar()
    vehicle_dropdown = ttk.Combobox(gv.rent_frame, textvariable=selected_vehicle)
    vehicle_dropdown['values'] = ('Car',
                                  'Small Van',
                                  'Big Van',
                                  '7 Seater',
                                  'Motorbike'
                                  )
    vehicle_dropdown['state'] = 'readonly'
    vehicle_dropdown.grid(row=1, column=1)

    # start date
    start_date = DateEntry(gv.rent_frame, locale='en_IE')
    start_date.grid(row=2, column=1)

    # end date
    end_date = DateEntry(gv.rent_frame, locale='en_IE')
    end_date.grid(row=3, column=1)

    gv.rent_data = {
        "userid": db.get_userid(),
        "location": selected_location.get(),
        "vehicle": selected_vehicle.get()
    }

    # rent button
    rent_button = tk.Button(gv.rent_frame, text="Submit", command=lambda: rent_car(selected_location.get(),
                                                                                   selected_vehicle.get(),
                                                                                   start_date.get_date(),
                                                                                   end_date.get_date()))
    rent_button.grid(row=5, column=1, columnspan=1, sticky="we", padx=5, pady=5)


def rent_car(location, vehicle, startdate, enddate):
    data = gv.rent_data
    data = {
        "userid": db.get_userid(),
        "location": location,
        "vehicle": vehicle,
        "startdate": startdate,
        "enddate": enddate
    }

    instance = db.DatabaseHandler('bookings', data)
    try:
        if instance.check_bookings() <= 1:
            raise errors.MaxLoansReached
        instance.add_booking()
    except (errors.MaxLoansReached, AssertionError) as e:
        print(f"{db.Colour.RED} {db.Colour.BOLD} User already has a vehicle on loan {db.Colour.END}")
        lbl_text = tk.Label(gv.rent_frame)
        lbl_text.grid(row=4, columnspan=2)
        lbl_text.config(text="You already have a vehicle on loan", fg="red")


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
