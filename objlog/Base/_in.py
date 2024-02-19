"""internals"""

class Mutable:
    # ignore me!
    __name__ = "Mutable"

class NoExceptionSpecified(Exception):
    __class__ = Mutable
    __class__.__name__ = "NoExceptionSpecified"
