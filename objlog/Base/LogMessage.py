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

    __slots__ = ('time_ns', 'message', '_unix', '_uuid', '_date_formatted')  # optimize memory usage

    def __init__(self, message):
        if self.color is None or self.level is None:
            raise TypeError("The color and level attributes must be set in the subclass.")
        self.time_ns = time_ns()
        self.message = str(message) if not isinstance(message, str) else message # only convert to str if not already a str (performance)
        self._unix = None
        # create uuid
        self._uuid = None
        # note: using ''.join is faster than f-strings or concatenation in a loop
        self._date_formatted =  None

    # lazy loading!
    @property
    def uuid(self):
        if self._uuid is None:
            self._uuid = '-'.join([str(self.time_ns), str(random.randint(0, 1000))])  # performance anywhere we can
        return self._uuid

    @property
    def date_formatted(self):
        if self._date_formatted is None:
            self._date_formatted = ''.join([strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.unix / 1000)), ".", f"{self.unix % 1000:03d}"])
        return self._date_formatted

    @property
    def unix(self) -> int:
        """
        The unix timestamp of the message in milliseconds.

        :return: The unix timestamp in milliseconds.
        """
        if self._unix is None:
            self._unix = self.time_ns // 1_000_000  # convert to milliseconds
        return self._unix


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
