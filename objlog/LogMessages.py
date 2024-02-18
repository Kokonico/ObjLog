"""the default log messages"""
from .Base import LogMessage, _in


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


class _PythonExceptionMessage(LogMessage):
    """A custom message class for exceptions"""
    exception = _in.NoExeptionSpecified
    level = f"PYTHON EXCEPTION ({exception.__class__.__name__})"
    color = "\033[91m"  # red color
    message = "N/A"

    def __init__(self, exception: Exception):
        # Use traceback to get a string representation of the exception
        self.exception = exception
        # get the exception's message (reason)
        # ex: Division by zero
        self.message = str(exception)
        self.level = f"PYTHON EXCEPTION ({exception.__class__.__name__})"
        super().__init__(self.message)
