

from colorist import BrightColor as BColour
import logging

logging.basicConfig(level=logging.INFO, 
                    format=f"{BColour.BLACK}%(asctime)s{BColour.OFF} {BColour.CYAN}APP{BColour.OFF} %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

def log(message: str, level=logging.INFO, ):
    """
    Logs a message to the console with a timestamp.
    """
    # print(f"{BColour.BLACK}{datetime.datetime.now()}{BColour.OFF} {BColour.CYAN}APP{BColour.OFF} {message}")
    logging.log(level, message)
