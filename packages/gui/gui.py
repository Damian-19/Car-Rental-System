import sqlite3
import tkinter as tk

from packages.business import logic as main, globalVariables as gV
from packages.gui import dashboard as dashboardfunctions
from packages.database import db

global conn, cursor

# The frames below use various elements of the tkinter package to create the GUI panels
# These 5 lines create the main panel in which the login and register frames are contained side by side.
main_frame = tk.Frame(gV.root).grid(column=0, row=0)
login_frame = tk.Frame(main_frame, bd=2, highlightbackground="black", highlightthickness=2)
login_frame.grid(column=0, row=0, sticky='nsew', padx=2, pady=2)
register_frame = tk.Frame(main_frame, bd=2, highlightbackground="black", highlightthickness=2)
register_frame.grid(column=1, row=0, sticky='nsew', padx=2, pady=2)

title = tk.Label(login_frame, text="Login", font=('arial', 15))
title.grid(column=0, row=0, columnspan=2, padx=10, pady=10)

# login_frame 1 - login
username_label = tk.Label(login_frame, text="Username")
username_label.grid(column=0, row=1, padx=10, pady=10)

username_input = tk.Entry(login_frame, textvariable=gV.USERNAME)
username_input.grid(column=1, row=1, padx=10, pady=10)

password_label = tk.Label(login_frame, text="Password")
password_label.grid(column=0, row=2, padx=10, pady=10)

password_input = tk.Entry(login_frame, textvariable=gV.PASSWORD, show="*")
password_input.grid(column=1, row=2)

# register_frame - register
title = tk.Label(register_frame, text="Register", font=('arial', 15))
title.grid(column=0, row=0, columnspan=2, padx=10, pady=10)

username_label = tk.Label(register_frame, text="Username")
username_label.grid(column=0, row=1, padx=10, pady=10)

username_input = tk.Entry(register_frame, textvariable=gV.RUSERNAME)
username_input.grid(column=1, row=1, padx=5, pady=5)

firstname_label = tk.Label(register_frame, text="Firstname")
firstname_label.grid(column=0, row=2, padx=10, pady=10)

firstname_input = tk.Entry(register_frame, textvariable=gV.FIRSTNAME)
firstname_input.grid(column=1, row=2)

lastname_label = tk.Label(register_frame, text="Lastname")
lastname_label.grid(column=0, row=3, padx=10, pady=10)

lastname_input = tk.Entry(register_frame, textvariable=gV.LASTNAME)
lastname_input.grid(column=1, row=3)

email_label = tk.Label(register_frame, text="Email")
email_label.grid(column=0, row=4, padx=10, pady=10)

email_input = tk.Entry(register_frame, textvariable=gV.EMAIL)
email_input.grid(column=1, row=4)

phonenumber_label = tk.Label(register_frame, text="Phone number")
phonenumber_label.grid(column=0, row=5, padx=10, pady=10)

phonenumber_input = tk.Entry(register_frame, textvariable=gV.PHONENUMBER)
phonenumber_input.grid(column=1, row=5)

password_label = tk.Label(register_frame, text="Password")
password_label.grid(column=0, row=6, padx=10, pady=10)

password_input = tk.Entry(register_frame, textvariable=gV.RPASSWORD, show="*")
password_input.grid(column=1, row=6)


def signout():
    gV.home.destroy()
    gV.root.deiconify()


def dashboard():
    gV.root.withdraw()
    gV.home = tk.Toplevel()
    gV.home.title("Dashboard")
    width = 300
    height = 250
    screen_width = gV.root.winfo_screenwidth()
    screen_height = gV.root.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    gV.root.resizable(0, 0)
    gV.home.geometry("%dx%d+%d+%d" % (width, height, x, y))
    # retrieve users firstname
    data = {
        "userid": db.get_userid()
    }
    name = db.DatabaseHandler('users', data).get_firstname()
    tk.Label(gV.home, text=f"Welcome, {str(name)}", font=('calibri', 20)).grid(column=0, row=0)
    dashboardfunctions.create_dashboard()
    tk.Button(gV.home, text='Sign Out', command=signout).grid(column=0, row=2)


def database():
    # create database connection
    global conn, cursor
    conn = sqlite3.connect(r"../../sqlite/db/database.db")
    cursor = conn.cursor()


def login():
    """
    function to login a user
    current params are all retrieved from global variables
    MVC - View
    """
    database()
    if gV.USERNAME.get() == "" or gV.PASSWORD.get() == "":
        lbl_text.config(text="Please fill out both fields.", fg="red")
    else:
        # place user-entered data into a dict
        logindata = {
            "username": gV.USERNAME.get(),
            "password": gV.PASSWORD.get()
        }
        # create instance of Login class
        instance = main.Login('users', logindata)
    try:
        # attempt to perform login
        instance.init_login()
        instance.login_cleanup()
        dashboard()
    except Exception as e:
        print(e)
        lbl_text.config(text="Invalid username or password", fg="red")


def register():
    """
    function to register a user in the database
    current params are all retrieved from global variables
    MVC - View
    """
    # check all fields are filled in
    if gV.RUSERNAME.get() == "" or gV.RPASSWORD.get() == "" or gV.FIRSTNAME.get() == "" or gV.LASTNAME.get() == "" or \
            gV.EMAIL.get() == "" or gV.PHONENUMBER.get() == "":
        lbl_register_text.config(text="Please fill in all fields.", fg="red")
    # perform register
    else:
        data = {
            "username": gV.RUSERNAME.get(),
            "firstname": gV.FIRSTNAME.get(),
            "lastname": gV.LASTNAME.get(),
            "email": gV.EMAIL.get(),
            "phone": gV.PHONENUMBER.get(),
            "password": gV.RPASSWORD.get()
        }
        instance = main.Register('users', data)
        try:
            instance.init_register()
            instance.register_cleanup()
            # successful register
            lbl_register_text.config(text="Signup successful. Please Login.", fg="green")
            # register failed
        except Exception as e:
            print(e)
            lbl_register_text.config(text="Username or email already in use", fg='red')
        print("Reached end of register function")


lbl_text = tk.Label(login_frame)
lbl_text.grid(row=3, columnspan=2)

button = tk.Button(login_frame, text="Login", command=login)
button.grid(column=0, row=4, columnspan=2, sticky="we", padx=10, pady=10)
button.bind('<Return>', login)

lbl_register_text = tk.Label(register_frame)
lbl_register_text.grid(row=7, columnspan=2)

register_button = tk.Button(register_frame, text="Sign Up", command=register)
register_button.grid(column=0, row=8, columnspan=2, sticky="we", padx=10, pady=10)

gV.root.title("CS4125")
gV.root.resizable(0, 0)
gV.root.mainloop()
