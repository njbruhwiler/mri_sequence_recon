# This script uses OLE Automation to write sequences on TNMR

import win32com.client as win32
from functions import str_to_float

# Connect to TNMR:
# (if you want to work with an existing file, make sure it's already open)
app = win32.Dispatch("NTNMR.Application")
active_doc_path = app.GetActiveDocPath
if active_doc_path == "":
    print("Creating new file")
else:
    print("Successfully linked to: ", active_doc_path)

# Set parameters:

# Echo time:
TE_input = float(input("Echo time (sec): "))
int_delay = str_to_float(app.GetNMRParameter("int_delay"))
tau = str_to_float(app.GetNMRParameter("tau"))
rd = str_to_float(app.GetNMRParameter("rd"))
ad = str_to_float(app.GetNMRParameter("ad"))
acq_time = str_to_float(app.GetNMRParameter("Acq. Time"))
last_delay = str_to_float(app.GetNMRParameter("Last Delay"))
extra = str_to_float("16u")
TE = int_delay + 2*tau + rd + ad
print(TE)
app.SetNMRParameter("int_delay", str(int_delay*TE_input/TE)+"s")
app.SetNMRParameter("tau", str(tau*TE_input/TE)+"s")
app.SetNMRParameter("rd", str(rd*TE_input/TE)+"s")
app.SetNMRParameter("ad", str(ad*TE_input/TE)+"s")

# Repetition time:
TR_input = float(input("Repetition time (sec): "))
TR = TE_input + acq_time + last_delay + extra
print(TR)
app.SetNMRParameter("Last Delay", str(last_delay-(TR-TR_input))+"s")

# Sweep width: 
SW_input = input("Sweep width (Hz): ")
app.SetNMRParameter("SW +/-", SW_input)

#Resolution:
#reso = input("Resolution (degrees): ")
