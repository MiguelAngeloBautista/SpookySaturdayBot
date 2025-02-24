# pylint: disable=all
from .logger import INFO_LOG, WARN_LOG, SUCCESS_LOG, DEBUG_LOG, ERROR_LOG, CRITICAL_LOG, log

DEBUG_LOG("Logger imported", context="SERVER")