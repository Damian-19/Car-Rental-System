import sqlite3
import tkinter as tk
from sqlite3 import Error

from packages.gui import dashboard as dashboardfunctions
from packages.business import main as main, globalVariables as gV

import packages.business.main

global conn, cursor

# frames
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


def back():
    gV.home.destroy()
    gV.root.deiconify()


def dashboard():
    gV.root.withdraw()
    gV.home = tk.Toplevel()
    gV.home.title("Dashboard")
    width = 600
    height = 500
    screen_width = gV.root.winfo_screenwidth()
    screen_height = gV.root.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    gV.root.resizable(0, 0)
    gV.home.geometry("%dx%d+%d+%d" % (width, height, x, y))
    # retrieve users firstname
    database()
    cursor.execute("SELECT Firstname FROM users WHERE username = ? ", (gV.USERNAME.get(),))
    name = cursor.fetchone()
    name = str(name).replace("(", "").replace(")", "").replace("'", "").replace(",", "")
    tk.Label(gV.home, text="Welcome, " + name, font=('calibri', 20)).grid(column=0, row=0)
    dashboardfunctions.create_dashboard()
    tk.Button(gV.home, text='Sign Out', command=back).grid(column=0, row=2)


def database():
    # create database connection
    global conn, cursor
    conn = sqlite3.connect(r"../../sqlite/db/database.db")
    cursor = conn.cursor()


def login():
    database()
    if gV.USERNAME.get() == "" or gV.PASSWORD.get() == "":
        lbl_text.config(text="Please fill out both fields.", fg="red")
    else:
        logindata = {"username": gV.USERNAME.get(), "password": gV.PASSWORD.get()}
        instance = main.Login('users', logindata)
    try:
        result = instance.init_login()
        instance.login_cleanup()
        lbl_text.config(text="Signup successful. Please Login.", fg="green")
    except Exception as e:
        print(e)
        lbl_text.config(text="Invalid username or password", fg="red")
    print("Reached end of login function")
   #     cursor.execute("SELECT salt, hashedPassword FROM users WHERE username = ? ",
   #                    (gV.USERNAME.get(),))
    #    salt, password = cursor.fetchone()
    #    print(type(salt))
        # salt = salt.encode(encoding='UTF=8')
    #    print(type(salt))
    #    print(type(password))
    #    try:
    #        assert main.check_password(salt, password, gV.PASSWORD.get())
     #       dashboard()
     #       gV.USERNAME.set("")
     #       gV.PASSWORD.set("")
     #       lbl_text.config(text="")
      #  except AssertionError:
       #     lbl_text.config(text="Invalid username or password", fg="red")
        #    gV.USERNAME.set("")
         #   gV.PASSWORD.set("")
    #cursor.close()
    #conn.close()


def register():
    """
    function to register a user in the database
    current params are all retrieved from global variables
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
# button.bind('<Return>', login())

lbl_register_text = tk.Label(register_frame)
lbl_register_text.grid(row=7, columnspan=2)

register_button = tk.Button(register_frame, text="Sign Up", command=register)
register_button.grid(column=0, row=8, columnspan=2, sticky="we", padx=10, pady=10)

gV.root.title("CS4125")
gV.root.resizable(0, 0)
gV.root.mainloop()
