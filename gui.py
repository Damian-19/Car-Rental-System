import tkinter as tk
import tkinter.ttk as ttk
import sqlite3
import db as db

root = tk.Tk()
USERNAME = tk.StringVar()
PASSWORD = tk.StringVar()
# frames
frame = tk.Frame(root, bd=2)
frame.grid(column=0, row=0, sticky='nsew')

# ==============================LABELS=========================================
title = tk.Label(frame, text="CS4125 Login", font=('arial', 15))
title.grid(column=0, row=0, columnspan=2, padx=10, pady=10)

firstname_label = tk.Label(frame, text="First Name")
firstname_label.grid(column=0, row=1, padx=10, pady=10)

username_input = tk.Entry(frame, textvariable=USERNAME)
username_input.grid(column=1, row=1)

password_label = tk.Label(frame, text="Password")
password_label.grid(column=0, row=2, padx=10, pady=10)

password_input = tk.Entry(frame, textvariable=PASSWORD, show="*")
password_input.grid(column=1, row=2)


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
        cursor.execute("SELECT * FROM `users` WHERE `firstName` = ? AND `password` = ?", (USERNAME.get(), PASSWORD.get()))
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


lbl_text = tk.Label(frame)
lbl_text.grid(row=3, columnspan=2)

button = tk.Button(frame, text="Login", command=Login)
button.grid(column=0, row=4, columnspan=2, sticky="we")
button.bind('<Return>', Login)

register_button = tk.Button(frame, text="Sign Up")
register_button.grid(column=0, row=5, columnspan=2, sticky="we")

"""tabs = ttk.Notebook(home)
catalog_frame = tk.Frame(tabs)
rent_frame = tk.Frame(tabs)
tabs.add(catalog_frame, text="Catalog")
tabs.add(rent_frame, text="Rent Car")"""

root.title("CS4125")
root.resizable(0, 0)
root.mainloop()
