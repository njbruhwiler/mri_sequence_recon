import tkinter as tk
from tkinter import ttk
import win32com.client as win32
from spin_echo import spin_echo


def check_connection():
    # Uses OLE Automation to connect to TNMR and displays active document path
    app = win32.Dispatch("NTNMR.Application")
    active_doc_path = app.GetActiveDocPath
    if active_doc_path == "":
        filename.configure(text="No open file found",
                           font=10,
                           foreground="red")
    else:
        filename.configure(text="\n\nSuccessfully linked to: " + str(active_doc_path), 
                           font=10,
                           foreground="green")
    
    # Buttons to choose sequence type to edit
    ttk.Label(w, text="\n\nSelect sequence type:\n", font=10).pack()
    ttk.Button(w, text="Spin echo", command=spin_echo).pack()


# Main window:
w = tk.Tk()
w.geometry("1000x400")
ttk.Label(w, text="Welcome!", font=10).pack()
ttk.Label(w, text="\n Open TNMR file to edit and click ok when done\n", font=10).pack()

ttk.Button(w, text="Ok", command=check_connection).pack()
filename = ttk.Label(w, text="")
filename.pack()

w.mainloop()

