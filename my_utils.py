# Useful functions

def str_to_float(string):
    # Takes a parameter from TNMR as a string and converts it to a float
    if string.endswith("s"):
        num = float(string[:-1])
    elif string.endswith("m"):
        num = float(string[:-1])/(10**3)
    elif string.endswith("u"):
        num = float(string[:-1])/(10**6)
    elif string.endswith("n"):
        num = float(string[:-1])/(10**9)
    return num









