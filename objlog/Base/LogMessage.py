"""a base message to be logged, WARNING: this class should not be used directly, use a subclass instead"""
import random
import time
from time import time_ns, strftime


class LogMessage:
    """
    A base message to be logged.

    WARNING: this class should not be used directly, use a subclass instead.

    :param message: The message to log.
    """

    color = None
    level = None
    exception = None  # for cleanliness (only used in PythonExceptionMessage subclass)
    # the reason for using None instead of not defining it is to avoid weird errors if the subclass doesn't define it.

    def __init__(self, message):
        if self.color is None or self.level is None:
            raise TypeError("The color and level attributes must be set in the subclass.")
        self.time_ns = time_ns()
        self.message = str(message)
        self.unix = self.time_ns // 1_000_000
        # create uuid
        self.uuid = f"{self.time_ns}-{random.randint(0, 1000)}"
        self.date_formatted = strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.unix / 1000))
        self.date_formatted = self.date_formatted + "." + f"{self.unix % 1000:03d}"

    def __str__(self):
        return f"[{self.date_formatted}] {self.level}: {self.message}"

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

        return f"{self.color}{self.__str__()}\033[0m"
