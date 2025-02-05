import pytest
from unittest.mock import patch
import logging
from colorist import BrightColor as BColour
from app.logger import log, INFO_LOG, WARN_LOG, DEBUG_LOG, ERROR_LOG, CRITICAL_LOG

@patch('app.logger.logger.logging.log')
def test_log_info(mock_log):
  log("This is an info message", "TEST", logging.INFO)
  mock_log.assert_called_once_with(logging.INFO, f'{BColour.BLUE}INFO{BColour.OFF} \t {BColour.CYAN}TEST{BColour.OFF} This is an info message')

@patch('app.logger.logger.logging.log')
def test_log_debug(mock_log):
  log("This is a debug message", "TEST", logging.DEBUG)
  mock_log.assert_called_once_with(logging.DEBUG, f'{BColour.GREEN}DEBUG{BColour.OFF} \t {BColour.CYAN}TEST{BColour.OFF} This is a debug message')

@patch('app.logger.logger.logging.log')
def test_log_warn(mock_log):
  log("This is a warn message", "TEST", logging.WARN)
  mock_log.assert_called_once_with(logging.WARN, f'{BColour.YELLOW}WARNING{BColour.OFF} \t {BColour.CYAN}TEST{BColour.OFF} This is a warn message')

@patch('app.logger.logger.logging.log')
def test_log_error(mock_log):
  log("This is an error message", "TEST", logging.ERROR)
  mock_log.assert_called_once_with(logging.ERROR, f'{BColour.RED}ERROR{BColour.OFF} \t {BColour.CYAN}TEST{BColour.OFF} This is an error message')

@patch('app.logger.logger.logging.log')
def test_log_critical(mock_log):
  log("This is a critical message", "TEST", logging.CRITICAL)
  mock_log.assert_called_once_with(logging.CRITICAL, f'{BColour.MAGENTA}CRITICAL{BColour.OFF} \t {BColour.CYAN}TEST{BColour.OFF} This is a critical message')

@patch('app.logger.logger.logging.log')
def test_info_log_partial(mock_log):
  INFO_LOG("This is an info message")
  mock_log.assert_called_once_with(logging.INFO, f'{BColour.BLUE}INFO{BColour.OFF} \t {BColour.CYAN}APP{BColour.OFF} This is an info message')

@patch('app.logger.logger.logging.log')
def test_warn_log_partial(mock_log):
  WARN_LOG("This is a warn message")
  mock_log.assert_called_once_with(logging.WARN, f'{BColour.YELLOW}WARNING{BColour.OFF} \t {BColour.CYAN}APP{BColour.OFF} This is a warn message')

@patch('app.logger.logger.logging.log')
def test_debug_log_partial(mock_log):
  DEBUG_LOG("This is a debug message")
  mock_log.assert_called_once_with(logging.DEBUG, f'{BColour.GREEN}DEBUG{BColour.OFF} \t {BColour.CYAN}APP{BColour.OFF} This is a debug message')

@patch('app.logger.logger.logging.log')
def test_error_log_partial(mock_log):
  ERROR_LOG("This is an error message")
  mock_log.assert_called_once_with(logging.ERROR, f'{BColour.RED}ERROR{BColour.OFF} \t {BColour.CYAN}APP{BColour.OFF} This is an error message')

@patch('app.logger.logger.logging.log')
def test_critical_log_partial(mock_log):
  CRITICAL_LOG("This is a critical message")
  mock_log.assert_called_once_with(logging.CRITICAL, f'{BColour.MAGENTA}CRITICAL{BColour.OFF} \t {BColour.CYAN}APP{BColour.OFF} This is a critical message')