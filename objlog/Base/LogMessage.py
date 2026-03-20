"""a base message to be logged, WARNING: this class should not be used directly, use a subclass instead"""

import random
from time import time_ns, strftime, localtime


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

    __slots__ = (
        "time_ns",
        "message",
        "_message",
        "_unix",
        "_uuid",
        "_date_formatted",
        "_formatted",
    )

    def __init__(self, message) -> None:
        if self.color is None or self.level is None:
            raise TypeError(
                "The color and level attributes must be set in the subclass."
            )
        self.time_ns = time_ns()
        self.message = (
            str(message) if not isinstance(message, str) else message
        )  # only convert to str if not already a str (performance)
        self._message = self.message  # backup for `fancy`'s lazy loading
        self._unix = None
        # create uuid
        self._uuid = None
        # note: using ''.join is faster than f-strings or concatenation in a loop
        self._date_formatted = None

        self._formatted = None

    # lazy loading!
    @property
    def uuid(self) -> str:
        if self._uuid is None:
            self._uuid = "-".join(
                [str(self.time_ns), str(random.randint(0, 1000))]
            )  # performance anywhere we can
        return self._uuid

    @property
    def formatted(self) -> str:
        """
        A fancy version of the message with ANSI and the date.
        :return: Formatted message.
        """
        if self._formatted is None or self._message != self.message:
            self._message = self.message
            return "".join([self.color, str(self), "\033[0m"])
        return self._formatted

    @property
    def date_formatted(self) -> str:
        if self._date_formatted is None:
            self._date_formatted = "".join(
                [
                    strftime("%Y-%m-%d %H:%M:%S", localtime(self.unix / 1000)),
                    ".",
                    f"{self.unix % 1000:03d}",
                ]
            )
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

    def __str__(self) -> str:
        return f"[{self.date_formatted}] {self.level}: {self.message}"

    def __repr__(self) -> str:
        return ": ".join([self.level, self.message])

    def __eq__(self, other) -> bool:
        if isinstance(other, LogMessage):
            return self.uuid == other.uuid
        else:
            return False

    def colored(self) -> str:
        """
        Returns a colored version of the message as a string.

        !DEPRECATED! Use `formatted` instead, it's identical.

        :return: The colored message.
        """
        return "".join([self.color, str(self), "\033[0m"])
