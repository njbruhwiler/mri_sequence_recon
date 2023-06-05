import tkinter as tk
from tkinter import ttk

m = tk.Tk()

def get_input():
    global TE_input
    global TR_input
    global SW_input
    TE_input=TE_entry.get()
    TR_input=TR_entry.get()
    SW_input=SW_entry.get()

ttk.Label(m, text="TE (sec)").grid(row=0)
TE_entry = tk.Entry(m)
TE_entry.grid(row=0, column=1)

ttk.Label(m, text="TR (sec)").grid(row=1)
TR_entry = tk.Entry(m)
TR_entry.grid(row=1, column=1)

ttk.Label(m, text="Sweep width (Hz)").grid(row=2)
SW_entry = tk.Entry(m)
SW_entry.grid(row=2, column=1)

ttk.Button(m, text="Okay", command=get_input).grid(row=3)
ttk.Button(m, text="Done", command=m.destroy).grid(row=4)

m.mainloop()

print("TE:", TE_input)
print("TR:", TR_input)
print("SW:", SW_input)
