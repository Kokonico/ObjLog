"""a base message to be logged, WARNING: this class should not be used directly, use a subclass instead"""
from datetime import datetime
from time import time_ns
import random


class LogMessage:
    """
    A base message to be logged.

    WARNING: this class should not be used directly, use a subclass instead.

    :param message: The message to log.
    """

    def __init__(self, message):
        self.message = str(message)
        self.unix = time_ns() // 1_000_000
        # create uuid
        self.uuid = f"{time_ns()}-{random.randint(0, 1000)}"
        try:
            self.color
            self.level
        except AttributeError:
            # because you cannot trust people (like myself) to read the docs
            # RTFM PEOPLE!!!
            # >:(((((( <- me rn, having to write this
            raise TypeError("this class should not be used directly, use a subclass instead")

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
        # and shave ms
        dt = datetime.fromtimestamp(self.unix / 1000)
        try:
            dt = dt.strftime("%Y-%m-%d %H:%M:%S")
        except ImportError:
            # python is likely shutting down
            dt = "TIME ERROR"
        return f"{self.color}[{dt}] {self.level}: {self.message}\033[0m"
