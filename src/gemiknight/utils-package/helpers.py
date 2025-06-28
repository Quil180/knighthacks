import datetime

def get_timestamp() -> str:

    # returns the current timestamp in a string 

    #str: A formatted timestamp (like "2023-10-27 15:45:01").

    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")