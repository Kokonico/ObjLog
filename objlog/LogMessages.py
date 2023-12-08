"""the default log messages"""
from .Base import LogMessage


class Debug(LogMessage):
    """the default debug message, with blue color"""
    level = "DEBUG"
    color = "\033[94m"


class Info(LogMessage):
    """the default info message, with green color"""
    level = "INFO"
    color = "\033[92m"


class Warn(LogMessage):
    """the default warn message, with yellow color"""
    level = "WARN"
    color = "\033[93m"


class Error(LogMessage):
    """the default error message, with red color"""
    level = "ERROR"
    color = "\033[91m"


class Fatal(LogMessage):
    """the default fatal message, with pink color"""
    level = "FATAL"
    color = "\033[95m"
