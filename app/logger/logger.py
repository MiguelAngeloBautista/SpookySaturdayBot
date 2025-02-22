"""
Logger module for the SpookySaturdayBot application.
"""

from functools import partial
import logging
from colorist import BrightColor as BColour
import inspect
import os


logging.basicConfig(level=logging.INFO,
                    format=f"{BColour.BLACK}%(asctime)s{BColour.OFF}"
                    f" %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

def get_context() -> str:
    stack = inspect.stack()
    for frame_info in stack:
        filename = os.path.basename(frame_info.filename)
        if filename != os.path.basename(__file__):
            return filename
    return "APP"

def log(message: str, context: str, level=logging.INFO) -> None:
    """
    Logs a message to the console with a timestamp.
    
    ### Args:
        `message (str)`: The message to log.
        `level (int)`: The logging level.
        
    ### Returns:
        None
    """
    if context is None:
        context = get_context()
    
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
INFO_LOG = lambda message, context=None: log(message, context=context, level=logging.INFO)
WARN_LOG = lambda message, context=None: log(message, context=context, level=logging.WARN)
DEBUG_LOG = lambda message, context=None: log(message, context=context, level=logging.DEBUG)
ERROR_LOG = lambda message, context=None: log(message, context=context, level=logging.ERROR)
CRITICAL_LOG = lambda message, context=None: log(message, context=context, level=logging.CRITICAL)