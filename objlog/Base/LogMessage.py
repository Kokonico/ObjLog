"""a base message to be logged, WARNING: this class should not be used directly, use a subclass instead"""
import sys
from datetime import datetime
from time import time_ns
import random


class LogMessage:
    """
    A base message to be logged.

    WARNING: this class should not be used directly, use a subclass instead.

    :param message: The message to log.
    """

    color = None
    level = None
    exception = None  # for cleanliness (only used in PythonExceptionMessage subclass)

    def __init__(self, message):
        self.message = str(message)
        self.unix = time_ns() // 1_000_000
        # create uuid
        self.uuid = f"{time_ns()}-{random.randint(0, 1000)}"
        if self.color is None or self.level is None:
            raise TypeError("The color and level attributes must be set in the subclass.")

    def __str__(self):
        dt = datetime.fromtimestamp(self.unix / 1000)
        return f"[{dt}] {self.level}: {self.message}"

    def __repr__(self):
        return f"{self.level}: {self.message}"

    def __eq__(self, other):
        return self.uuid == other.uuid

    def __ne__(self, other):
        return self.uuid != other.uuid

    def colored(self) -> str:
        """
        Returns a colored version of the message as a string.

        :return: The colored message.
        """
        # convert unix to datetime
        try:
            dt = datetime.fromtimestamp(self.unix / 1000)
            dt = str(dt)[:-3]
        except Exception as e:
            dt = f"TIME ERROR ({e.__class__.__name__})"

        return f"{self.color}[{dt}] {self.level}: {self.message}\033[0m"
