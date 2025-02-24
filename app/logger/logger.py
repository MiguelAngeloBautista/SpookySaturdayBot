"""
Logger module for the SpookySaturdayBot application.
"""

from loguru import logger
from colorist import BrightColor as BColour
import inspect
import os

def log(message: str, context: str = None, level: str = "INFO") -> None:
    """
    Logs a message using Loguru with the appropriate caller context.
    
    If context is not provided, it is automatically filled using get_context().
    Adjusting the stack level makes Loguru show the correct source location.
    
    Args:
        message (str): The message to log.
        context (str, optional): The logging context.
        level (str): The logging level.
    """
    if context is None:
        context = get_context()
    final_message = f"[{context}] {message}"

    # Adjust the stack depth so that Loguru's record shows the correct caller.
    depth = 2

    match level.upper():
        case "DEBUG":
            logger.opt(depth=depth).debug(final_message)
        case "INFO":
            logger.opt(depth=depth).info(final_message)
        case "SUCCESS":
            logger.opt(depth=depth).success(final_message)
        case "WARNING":
            logger.opt(depth=depth).warning(final_message)
        case "ERROR":
            logger.opt(depth=depth).error(final_message)
        case "CRITICAL":
            logger.opt(depth=depth).critical(final_message)
        case _:
            logger.opt(depth=depth).info(final_message)

def get_context() -> str:
    stack = inspect.stack()
    for frame_info in stack:
        filename = os.path.basename(frame_info.filename)
        if filename != os.path.basename(__file__):
            return filename
    return "APP"

INFO_LOG = lambda message, context=None: log(message, context=context, level="INFO")
SUCCESS_LOG = lambda message, context=None: log(message, context=context, level="SUCCESS")
WARN_LOG = lambda message, context=None: log(message, context=context, level="WARNING")
DEBUG_LOG = lambda message, context=None: log(message, context=context, level="DEBUG")
ERROR_LOG = lambda message, context=None: log(message, context=context, level="ERROR")
CRITICAL_LOG = lambda message, context=None: log(message, context=context, level="CRITICAL")