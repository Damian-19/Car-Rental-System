# importing various required packages
import sqlite3
import tkinter as tk
import tkinter.ttk as ttk

from tkcalendar import DateEntry

from packages.business import errors
from packages.business import globalVariables as gv
from packages.business import logic
from packages.database import db


def database():
    # create database connection.
    global conn, cursor
    conn = sqlite3.connect(r"../../sqlite/db/database.db")
    cursor = conn.cursor()


def begin_edit(button_name, save_info_button):
    button_name.config(state='normal')
    save_info_button.config(state='normal')

# create dashboard page (displayed after login)


def create_dashboard():
    tabs = ttk.Notebook(gv.home)
    gv.home.resizable(0, 0)

    # creates a tabs layout for pages on the dashboard
    gv.booking_frame = tk.Frame(tabs)
    gv.rent_frame = tk.Frame(tabs)
    gv.account_frame = tk.Frame(tabs)

    # ordering the tabs through a grid based process
    gv.booking_frame.grid(column=0, row=0)
    gv.rent_frame.grid(column=1, row=0)
    gv.account_frame.grid(column=3, row=0)

    tabs.add(gv.booking_frame, text="Bookings")
    tabs.add(gv.rent_frame, text="Rent Car")
    tabs.add(gv.account_frame, text="Account")

    tabs.grid(column=0, row=1)
    populate_account()
    rent_tab()
    bookings_tab()

# bookings page function which allows the user to see the cars they are currently renting
def bookings_tab():
    con = sqlite3.connect(r"../../sqlite/db/database.db")
    new_cursor = con.cursor()
    new_cursor.execute("SELECT startDate, endDate FROM bookings WHERE userid = ?",
                       (db.get_userid(),))
    result = new_cursor.fetchall()

    if len(result) > 0:
        result = list(result[0])
        result[0] = result[0].replace("-", "/")
        result[1] = result[1].replace("-", "/")
        tk.Label(gv.booking_frame, text="Current Bookings").grid(row=0, column=0)
        tk.Label(gv.booking_frame, text=f"  {result[0]} - {result[1]}").grid(row=2, column=0)

    else:
        tk.Label(gv.booking_frame, text="You have no vehicles currently on loan").grid(row=1, column=0)

# function to rent a car, given the options 'location' and 'Vehicle' and the desired dates
def rent_tab():
    gv.rent_data = {}
    tk.Label(gv.rent_frame, text="Location").grid(row=0, column=0)
    tk.Label(gv.rent_frame, text="Vehicle Type").grid(row=1, column=0)
    tk.Label(gv.rent_frame, text="Start Date").grid(row=2, column=0)
    tk.Label(gv.rent_frame, text="End Date").grid(row=3, column=0)

    # location dropdown
    selected_location = tk.StringVar()
    location_dropdown = ttk.Combobox(gv.rent_frame, textvariable=selected_location)
    location_dropdown['values'] = ('Select Location',
                                   'Cork',
                                   'Limerick',
                                   'Dublin',
                                   'Waterford')
    location_dropdown['state'] = 'readonly'
    location_dropdown.grid(row=0, column=1)

    # vehicle dropdown which gives avaliable vehicle options
    selected_vehicle = tk.StringVar()
    vehicle_dropdown = ttk.Combobox(gv.rent_frame, textvariable=selected_vehicle)
    vehicle_dropdown['values'] = ('Select Vehicle',
                                  'Car',
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
    if location == "" or location == "Select Location" or vehicle == "" or vehicle == "Select Vehicle":
        lbl_text = tk.Label(gv.rent_frame)
        lbl_text.grid(row=4, columnspan=2)
        lbl_text.config(text="")
        lbl_text.config(text="Please fill out all fields", fg="red")
        return
    else:
        data = {
            "userid": db.get_userid(),
            "location": location,
            "vehicle": vehicle,
            "startdate": startdate,
            "enddate": enddate
        }

    instance = db.DatabaseHandler('bookings', data)
    lbl_text = tk.Label(gv.rent_frame)
    lbl_text.grid(row=4, columnspan=2)
    try:
        if instance.check_bookings() == 1:
            raise errors.MaxLoansReached
        points_instance = logic.BusinessLogic(data)
        points_earned = points_instance.calculate_points()
        instance.add_booking()
        bookings_tab()
        popupmsg("Booking Successful", f"You earned {points_earned:.2f} points!")
    except (errors.MaxLoansReached, AssertionError):
        print(f"{db.Colour.RED} {db.Colour.BOLD} User already has a vehicle on loan {db.Colour.END}")
        lbl_text.config(text="You already have a vehicle on loan", fg="red")
    except errors.NegativeDaysReached:
        print(f"{db.Colour.RED} {db.Colour.BOLD} Please select a valid date range {db.Colour.END}")
        popupmsg("Warning", f"Please select a valid date range")

# function for the pop up message showing which shows user how many points they earned from booking


def popupmsg(title, msg):
    popup = tk.Tk()
    popup.geometry("300x90")
    popup.wm_title(title)
    label = ttk.Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    button = ttk.Button(popup, text="Okay", command=popup.destroy)
    button.pack()
    popup.mainloop()

# Funcion to edit account details


def populate_account():
    database()
    # creates option to edit first name in the account tab of the dashboard
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

    # creates option to edit last name in the account tab of the dashboard
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
