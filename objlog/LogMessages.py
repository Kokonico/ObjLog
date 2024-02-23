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


class PythonExceptionMessage(LogMessage):
    """A custom message class for exceptions, not for general use.
    It's used to allow python exceptions to be logged with objlog."""
    exception = _in.NoExceptionSpecified
    level = f"PYTHON EXCEPTION (UNSPECIFIED)"
    color = "\033[91m"  # red color
    message = "N/A"

    def __init__(self, exception: Exception):
        # Use traceback to get a string representation of the exception
        self.exception = exception
        # get the location of the exception (if possible)
        # ex: foo.py, line 3, in divide_by_zero
        try:
            self.location = f"{self.exception.__traceback__.tb_frame.f_code.co_filename}, line {self.exception.__traceback__.tb_lineno}, in {self.exception.__traceback__.tb_frame.f_code.co_name}"
        except AttributeError:
            # if the location can't be found, set it to "N/A"
            self.location = "N/A"
        self.level = "PYTHON EXCEPTION (" + exception.__class__.__name__ + ")"
        # get the exception's message (reason)
        # ex: Division by zero
        self.message = str(exception) + f" ({self.location})"
        super().__init__(self.message)
