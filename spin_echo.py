import tkinter as tk
from tkinter import ttk
import win32com.client as win32
from my_utils import str_to_float

# Functions to edit spin echo sequence parameters

def spin_echo():
    # This function creates window with SE parameters and takes user input to change them
    
    # Create window
    m = tk.Tk()
    m.geometry("1000x400")

    # Set up grid:
    for i in range(10):
        m.rowconfigure(i, minsize=50)
    for i in range(10):
        m.columnconfigure(i, minsize=150)

    # Current parameter values:
    ttk.Label(m, text="Current values:").grid(row=0, column=1)
    ttk.Label(m, text="TE (sec)").grid(row=1)
    ttk.Label(m, text="TR (sec)").grid(row=2)
    ttk.Label(m, text="Sweep width (Hz)").grid(row=3)

    current_TE, current_TR, current_SW = get_SE_parameters()
    global current_TE_label
    global current_TR_label
    global current_SW_label
    current_TE_label = tk.Label(m, text=current_TE)
    current_TR_label = tk.Label(m, text=current_TR)
    current_SW_label = tk.Label(m, text=current_SW)
    current_TE_label.grid(row=1,column=1)
    current_TR_label.grid(row=2,column=1)
    current_SW_label.grid(row=3,column=1)

    # Input parameter values:
    ttk.Label(m, text="Inputs:").grid(row=0, column=2)

    global TE_entry
    global TR_entry
    global SW_entry
    TE_entry = tk.Entry(m)
    TR_entry = tk.Entry(m)
    SW_entry = tk.Entry(m)
    TE_entry.grid(row=1, column=2)
    TR_entry.grid(row=2, column=2)
    SW_entry.grid(row=3, column=2)

    # New values:
    ttk.Label(m, text="New values:").grid(row=0, column=3)

    global new_TE_label
    global new_TR_label
    global new_SW_label
    new_TE_label = tk.Label(m, text="")
    new_TR_label = tk.Label(m, text="")
    new_SW_label = tk.Label(m, text="")
    new_TE_label.grid(row=1,column=3)
    new_TR_label.grid(row=2,column=3)
    new_SW_label.grid(row=3,column=3)

    # Buttons:
    ttk.Button(m, text="Okay", command=update_parameters).grid(row=4, column=1, columnspan=2)
    ttk.Button(m, text="Done", command=m.destroy).grid(row=5, column=1, columnspan=2)

    m.mainloop()


def update_parameters():
    # This function is called when the "Okay" button is pressed and it updates the current parameters,
    # takes the user input and outputs the changed parameters

    # Update current parameters
    current_TE, current_TR, current_SW = get_SE_parameters()
    current_TE_label.configure(text=current_TE)
    current_TR_label.configure(text=current_TR)
    current_SW_label.configure(text=current_SW)

    # Get user input and change parameters in TNMR
    TE_input=float(TE_entry.get())
    TR_input=float(TR_entry.get())
    SW_input=float(SW_entry.get())
    change_SE_parameters(TE_input,TR_input,SW_input)

    # Display changed parameter values
    new_TE, new_TR, new_SW = get_SE_parameters()
    new_TE_label.configure(text=new_TE)
    new_TR_label.configure(text=new_TR)
    new_SW_label.configure(text=new_SW)


def get_SE_parameters():
    # Uses OLE Automation to access SE parameters on TNMR

    # Connect to TNMR:
    # (if you want to work with an existing file, make sure it's already open)
    app = win32.Dispatch("NTNMR.Application")

    # Get parameters:
    # Echo time:
    T90 = str_to_float(app.GetNMRParameter("T90"))
    T180 = str_to_float(app.GetNMRParameter("T180"))
    tau = str_to_float(app.GetNMRParameter("tau"))
    rd = str_to_float(app.GetNMRParameter("rd"))
    ad = str_to_float(app.GetNMRParameter("ad"))
    acq_time = str_to_float(app.GetNMRParameter("Acq. Time"))
    last_delay = str_to_float(app.GetNMRParameter("Last Delay"))
    extra1 = str_to_float("10u")
    extra2 = str_to_float("16u")
    TE = T90 + T180 + 2*tau + rd + ad + extra1

    # Repetition time:
    TR = TE + acq_time + last_delay + extra2

    # Sweep width: 
    SW = app.GetNMRParameter("SW +/-")

    return TE, TR, SW


def change_SE_parameters(TE_input, TR_input, SW_input):
    # Uses OLE Automation to change SE parameters on TNMR

    # Connect to TNMR:
    # (if you want to work with an existing file, make sure it's already open)
    app = win32.Dispatch("NTNMR.Application")

    # Set parameters:
    # Sweep width: 
    SW = get_SE_parameters()[2]
    app.SetNMRParameter("SW +/-", SW_input)

    # Echo time:
    T90 = str_to_float(app.GetNMRParameter("T90"))
    T180 = str_to_float(app.GetNMRParameter("T180"))
    tau = str_to_float(app.GetNMRParameter("tau"))
    rd = str_to_float(app.GetNMRParameter("rd"))
    ad = str_to_float(app.GetNMRParameter("ad"))
    acq_time = str_to_float(app.GetNMRParameter("Acq. Time"))
    last_delay = str_to_float(app.GetNMRParameter("Last Delay"))
    extra1 = str_to_float("10u")
    extra2 = str_to_float("16u")
    TE = get_SE_parameters()[0]
    app.SetNMRParameter("T90", str(T90*(TE_input-extra1)/(TE-extra1))+"s")
    app.SetNMRParameter("T180", str(T180*(TE_input-extra1)/(TE-extra1))+"s")
    app.SetNMRParameter("tau", str(tau*(TE_input-extra1)/(TE-extra1))+"s")
    app.SetNMRParameter("rd", str(rd*(TE_input-extra1)/(TE-extra1))+"s")
    app.SetNMRParameter("ad", str(ad*(TE_input-extra1)/(TE-extra1))+"s")

    # Repetition time:
    TR = get_SE_parameters()[1]
    app.SetNMRParameter("Last Delay", str(last_delay-(TR-TR_input))+"s")