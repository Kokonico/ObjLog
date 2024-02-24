"""internals"""


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
