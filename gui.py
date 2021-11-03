import tkinter as tk
import tkinter.ttk as ttk
import sqlite3
from sqlite3 import Error
import db as db

root = tk.Tk()
USERNAME = tk.StringVar()
PASSWORD = tk.StringVar()

FIRSTNAME = tk.StringVar()
LASTNAME = tk.StringVar()
EMAIL = tk.StringVar()
PHONENUMBER = tk.StringVar()
# frames
frame = tk.Frame(root, bd=2)
frame.grid(column=0, row=0, sticky='nsew')
frame2 = tk.Frame(root, bd=2)
frame2.grid(column=1, row=0, sticky='nsew')
# ==============================LABELS=========================================
title = tk.Label(frame, text="Login", font=('arial', 15))
title.grid(column=0, row=0, columnspan=2, padx=10, pady=10)


# frame 1
username_label = tk.Label(frame, text="Username")
username_label.grid(column=0, row=1, padx=10, pady=10)

username_input = tk.Entry(frame, textvariable=USERNAME)
username_input.grid(column=1, row=1)

password_label = tk.Label(frame, text="Password")
password_label.grid(column=0, row=2, padx=10, pady=10)

password_input = tk.Entry(frame, textvariable=PASSWORD, show="*")
password_input.grid(column=1, row=2)

# frame2
title = tk.Label(frame2, text="Register", font=('arial', 15))
title.grid(column=0, row=0, columnspan=2, padx=10, pady=10)

username_label = tk.Label(frame2, text="Username")
username_label.grid(column=0, row=1, padx=10, pady=10)
username_input = tk.Entry(frame2, textvariable=USERNAME)
username_input.grid(column=1, row=1)

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

password_input = tk.Entry(frame2, textvariable=PASSWORD, show="*")
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
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.resizable(0, 0)
    home.geometry("%dx%d+%d+%d" % (width, height, x, y))
    lbl_home = tk.Label(home, text="Welcome, " + str(USERNAME.get()), font=('calibri', 20)).pack()
    btn_back = tk.Button(home, text='Sign Out', command=Back).pack(pady=20, fill='x')


def database():
    global conn, cursor
    conn = sqlite3.connect(r"sqlite/db/database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `users` WHERE `firstName` = 'admin' AND `password` = 'admin'")

def Login():
    database()
    if USERNAME.get() == "" or PASSWORD.get() == "":
        lbl_text.config(text="Please fill out both fields.", fg="red")
    else:
        cursor.execute("SELECT * FROM `users` WHERE `username` = ? AND `password` = ?", (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:
            dashboard()
            USERNAME.set("")
            PASSWORD.set("")
            lbl_text.config(text="")
        else:
            lbl_text.config(text="Invalid username or password", fg="red")
            USERNAME.set("")
            PASSWORD.set("")
    cursor.close()
    conn.close()

def Register():
    database()
    if USERNAME.get() == "" or PASSWORD.get() == "" or FIRSTNAME.get() == "" or LASTNAME.get() == "" \
            or EMAIL.get() == "" or PHONENUMBER.get() == "":
        lbl_text.config(text="Please fill out all fields.", fg="red")
    else:
        cursor.execute("SELECT * FROM `users` WHERE `username` = ? AND `email` = ?", (USERNAME.get(), EMAIL.get()))
        if cursor.fetchone() is not None:
            lbl_text.config(text="User already exists")
        else:
            try:
                cursor.execute("INSERT INTO 'users' (username, firstName, lastName, email, phoneNumber, password) VALUES(?,?,?,?,?,?)",
                           (USERNAME.get(), FIRSTNAME.get(), LASTNAME.get(), EMAIL.get(), PHONENUMBER.get(), PASSWORD.get()))
            except Error as e:
                print("Error: ", e)
    cursor.close()
    conn.close()


lbl_text = tk.Label(frame)
lbl_text.grid(row=3, columnspan=2)

button = tk.Button(frame, text="Login", command=Login)
button.grid(column=0, row=4, columnspan=2, sticky="we")
button.bind('<Return>', Login)

register_button = tk.Button(frame2, text="Sign Up", command=Register)
register_button.grid(column=0, row=7, columnspan=2, sticky="we")

"""tabs = ttk.Notebook(home)
catalog_frame = tk.Frame(tabs)
rent_frame = tk.Frame(tabs)
tabs.add(catalog_frame, text="Catalog")
tabs.add(rent_frame, text="Rent Car")"""

root.title("CS4125")
root.resizable(0, 0)
root.mainloop()
