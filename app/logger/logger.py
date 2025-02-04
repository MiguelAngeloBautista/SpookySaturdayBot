"""
Logger module for the SpookySaturdayBot application.
"""

import logging
from colorist import BrightColor as BColour


logging.basicConfig(level=logging.INFO,
                    format=f"{BColour.BLACK}%(asctime)s{BColour.OFF}"
                    f" %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

def log(context: str, message: str, level=logging.INFO, ) -> None:
    """
    Logs a message to the console with a timestamp.
    
    ### Args:
        `message (str)`: The message to log.
        `level (int)`: The logging level.
        
    ### Returns:
        None
    """

    final_message = f"{BColour.BLUE}{logging.getLevelName(level)}{BColour.OFF} " \
                    f"\t {BColour.CYAN}{context}{BColour.OFF} {message}"
    logging.log(level, final_message)
