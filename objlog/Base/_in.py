"""internals"""

class Mutable:
    # ignore me!
    __name__ = "Mutable"

class NoExeptionSpecified(Exception):
    __class__ = Mutable
    __class__.__name__ = "NoExeptionSpecified"
