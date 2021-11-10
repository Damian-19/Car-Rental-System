from packages.business import globalVariables as gV
import tkinter as tk


def form():
    tk.Label(gV.rent_frame, text="Type of Vehicle").grid(column=0, row=0, padx=5, pady=5)
    vehicle_options = ['Select Option', '3-Door Car', '5-Door Car', 'Small Van', 'Large Van']
    var = tk.StringVar()
    var.set(vehicle_options[0])
    tk.OptionMenu(gV.rent_frame, var).grid(column=1, row=0)
    # type of vehicle dropdown
    # length of rent period
    # location
    # price estimation


form()
