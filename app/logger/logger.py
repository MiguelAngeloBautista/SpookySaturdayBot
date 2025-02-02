
import datetime
from colorist import BrightColor as BColour

def log(message):
    """
    Logs a message to the console with a timestamp.
    """
    print(f"{BColour.BLACK}{datetime.datetime.now()}{BColour.OFF} {BColour.CYAN}APP{BColour.OFF} {message}")
