import tkinter as tk
import tkinter.ttk as ttk
import sqlite3
from sqlite3 import Error
import db as db
import main as main
import hmac

root = tk.Tk()

# login variables
USERNAME = tk.StringVar()
PASSWORD = tk.StringVar()

# register variables
RUSERNAME = tk.StringVar()
RPASSWORD = tk.StringVar()
FIRSTNAME = tk.StringVar()
LASTNAME = tk.StringVar()
EMAIL = tk.StringVar()
PHONENUMBER = tk.StringVar()

# frames
main_frame = tk.Frame(root).grid(column=0, row=0)
frame = tk.Frame(main_frame, bd=2, highlightbackground="black", highlightthickness=2)
frame.grid(column=0, row=0, sticky='nsew', padx=2, pady=2)
frame2 = tk.Frame(main_frame, bd=2, highlightbackground="black", highlightthickness=2)
frame2.grid(column=1, row=0, sticky='nsew', padx=2, pady=2)
# ==============================LABELS=========================================
title = tk.Label(frame, text="Login", font=('arial', 15))
title.grid(column=0, row=0, columnspan=2, padx=10, pady=10)

# frame 1 - login
username_label = tk.Label(frame, text="Username")
username_label.grid(column=0, row=1, padx=10, pady=10)

username_input = tk.Entry(frame, textvariable=USERNAME)
username_input.grid(column=1, row=1, padx=10, pady=10)

password_label = tk.Label(frame, text="Password")
password_label.grid(column=0, row=2, padx=10, pady=10)

password_input = tk.Entry(frame, textvariable=PASSWORD, show="*")
password_input.grid(column=1, row=2)

# frame2 - register
title = tk.Label(frame2, text="Register", font=('arial', 15))
title.grid(column=0, row=0, columnspan=2, padx=10, pady=10)

username_label = tk.Label(frame2, text="Username")
username_label.grid(column=0, row=1, padx=10, pady=10)

username_input = tk.Entry(frame2, textvariable=RUSERNAME)
username_input.grid(column=1, row=1, padx=5, pady=5)

firstname_label = tk.Label(frame2, text="Firstname")
firstname_label.grid(column=0, row=2, padx=10, pady=10)

firstname_input = tk.Entry(frame2, textvariable=FIRSTNAME)
firstname_input.grid(column=1, row=2)

lastname_label = tk.Label(frame2, text="Lastname")
lastname_label.grid(column=0, row=3, padx=10, pady=10)

lastname_input = tk.Entry(frame2, textvariable=LASTNAME)
lastname_input.grid(column=1, row=3)

email_label = tk.Label(frame2, text="Email")
email_label.grid(column=0, row=4, padx=10, pady=10)

email_input = tk.Entry(frame2, textvariable=EMAIL)
email_input.grid(column=1, row=4)

phonenumber_label = tk.Label(frame2, text="Phone number")
phonenumber_label.grid(column=0, row=5, padx=10, pady=10)

phonenumber_input = tk.Entry(frame2, textvariable=PHONENUMBER)
phonenumber_input.grid(column=1, row=5)

password_label = tk.Label(frame2, text="Password")
password_label.grid(column=0, row=6, padx=10, pady=10)

password_input = tk.Entry(frame2, textvariable=RPASSWORD, show="*")
password_input.grid(column=1, row=6)


def Back():
    home.destroy()
    root.deiconify()


def dashboard():
    global home
    root.withdraw()
    home = tk.Toplevel()
    home.title("Dashboard")
    width = 600
    height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.resizable(0, 0)
    home.geometry("%dx%d+%d+%d" % (width, height, x, y))
    lbl_home = tk.Label(home, text="Welcome, " + str(USERNAME.get()), font=('calibri', 20)).pack()
    btn_back = tk.Button(home, text='Sign Out', command=Back).pack(pady=20, fill='x')


def database():
    global conn, cursor
    conn = sqlite3.connect(r"sqlite/db/database.db")
    cursor = conn.cursor()
    #cursor.execute("SELECT * FROM `users` WHERE `firstName` = 'admin' AND `password` = 'admin'")


def login():
    database()
    if USERNAME.get() == "" or PASSWORD.get() == "":
        lbl_text.config(text="Please fill out both fields.", fg="red")
    else:
        cursor.execute("SELECT salt, hashedPassword FROM users WHERE username = ? ",
                       (USERNAME.get(),))
        salt, password = cursor.fetchone()
        print(type(salt))
        #salt = salt.encode(encoding='UTF=8')
        print(type(salt))
        print(type(password))
        try:
            assert main.check_password(salt, password, PASSWORD.get())
            dashboard()
            USERNAME.set("")
            PASSWORD.set("")
            lbl_text.config(text="")
        except AssertionError as e:
            lbl_text.config(text="Invalid username or password", fg="red")
            USERNAME.set("")
            PASSWORD.set("")
    cursor.close()
    conn.close()


def register():
    database()
    if RUSERNAME.get() == "" or RPASSWORD.get() == "" or FIRSTNAME.get() == "" or LASTNAME.get() == "" or EMAIL.get() == "" or PHONENUMBER.get() == "":
        lbl_text.config(text="Please fill in all fields.", fg="red")
    else:
        cursor.execute("SELECT * FROM `users` WHERE `username` = ? AND `email` = ?", (RUSERNAME.get(), EMAIL.get()))
        if cursor.fetchone() is not None:
            lbl_text.config(text="User already exists")
        else:
            salt, password_hash = main.hash_password(RPASSWORD.get())
            try:
                cursor.execute(
                    "INSERT INTO 'users' (username, firstName, lastName, email, phoneNumber, salt, hashedPassword) "
                    "VALUES(?,?,?,?,?,?,?)",
                    (RUSERNAME.get(), FIRSTNAME.get(), LASTNAME.get(), EMAIL.get(), PHONENUMBER.get(), salt,
                     password_hash))
                conn.commit()
            except Error as e:
                print("Error: ", e)
    cursor.close()
    conn.close()


lbl_text = tk.Label(frame)
lbl_text.grid(row=3, columnspan=2)

button = tk.Button(frame, text="Login", command=login)
button.grid(column=0, row=4, columnspan=2, sticky="we", padx=10, pady=10)
button.bind('<Return>', login())

register_button = tk.Button(frame2, text="Sign Up", command=register)
register_button.grid(column=0, row=7, columnspan=2, sticky="we", padx=10, pady=10)

"""tabs = ttk.Notebook(home)
catalog_frame = tk.Frame(tabs)
rent_frame = tk.Frame(tabs)
tabs.add(catalog_frame, text="Catalog")
tabs.add(rent_frame, text="Rent Car")"""

root.title("CS4125")
root.resizable(0, 0)
root.mainloop()
