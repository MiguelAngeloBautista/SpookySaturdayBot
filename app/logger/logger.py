"""
Logger module for the SpookySaturdayBot application.
"""

from functools import partial
import logging
from colorist import BrightColor as BColour


logging.basicConfig(level=logging.INFO,
                    format=f"{BColour.BLACK}%(asctime)s{BColour.OFF}"
                    f" %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

def log(message: str, context: str, level=logging.INFO) -> None:
    """
    Logs a message to the console with a timestamp.
    
    ### Args:
        `message (str)`: The message to log.
        `level (int)`: The logging level.
        
    ### Returns:
        None
    """
    match level:
        case logging.DEBUG:
            final_message = f"{BColour.GREEN}{logging.getLevelName(level)}{BColour.OFF} " \
                            f"\t {BColour.CYAN}{context}{BColour.OFF} {message}"
        case logging.INFO:
            final_message = f"{BColour.BLUE}{logging.getLevelName(level)}{BColour.OFF} " \
                            f"\t {BColour.CYAN}{context}{BColour.OFF} {message}"
        case logging.WARN:
            final_message = f"{BColour.YELLOW}{logging.getLevelName(level)}{BColour.OFF} " \
                            f"\t {BColour.CYAN}{context}{BColour.OFF} {message}"
        case logging.ERROR:
            final_message = f"{BColour.RED}{logging.getLevelName(level)}{BColour.OFF} " \
                            f"\t {BColour.CYAN}{context}{BColour.OFF} {message}"
        case logging.CRITICAL:
            final_message = f"{BColour.MAGENTA}{logging.getLevelName(level)}{BColour.OFF} " \
                            f"\t {BColour.CYAN}{context}{BColour.OFF} {message}"

    logging.log(level, final_message)

# Level Based Partial Functions
INFO_LOG = partial(log, context="APP", level=logging.INFO)
WARN_LOG = partial(log, context="APP", level=logging.WARN)
DEBUG_LOG = partial(log, context="APP", level=logging.DEBUG)
ERROR_LOG = partial(log, context="APP", level=logging.ERROR)
CRITICAL_LOG = partial(log, context="APP", level=logging.CRITICAL)
