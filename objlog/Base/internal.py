"""internals"""
from . import LogMessage


class Mutable:
    """
    Mutable class for stuff.
    """
    # ignore me!
    __name__ = "Mutable"


class NoExceptionSpecified(Exception):
    """
    For PythonExceptionMessage class.
    """
    __class__ = Mutable
    __class__.__name__ = "NoExceptionSpecified"

class ObjLogInternalError(LogMessage):
    """
    An internal ObjLog error.
    """
    level = "OBJLOG INTERNAL ERROR"
    color = "\033[91m"  # red color

    def __init__(self, message: str):
        """
        :param message: The internal error message.
        """
        super().__init__(message)
