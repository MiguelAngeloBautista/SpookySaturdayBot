# pylint: disable=all
from .logger import INFO_LOG, WARN_LOG, DEBUG_LOG, ERROR_LOG, CRITICAL_LOG, log

INFO_LOG("Logger imported", context="SERVER")