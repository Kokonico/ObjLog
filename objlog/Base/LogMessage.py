"""a base message to be logged, WARNING: this class should not be used directly, use a subclass instead"""
from datetime import datetime
from time import time_ns
import random


class LogMessage:
    """a base message to be logged
    Attributes:
        color
        level (name)

    WARNING: this class should not be used directly, use a subclass instead
    it is designed to be used as a base class for other classes, and will not work properly if used directly.
    """

    def __init__(self, message):
        self.message = message
        self.timestamp = datetime.now()
        self.unix_timestamp = time_ns() // 1_000_000
        # create uuid
        self.uuid = f"{time_ns()}-{random.randint(0, 1000)}"

    def __str__(self):
        return f"[{self.timestamp}] {self.level}: {self.message}"

    def __repr__(self):
        return f"{self.level}: {self.message}"

    def __eq__(self, other):
        return self.uuid == other.uuid

    def colored(self) -> str:
        """return a colored version of the message"""
        return f"{self.color}[{self.timestamp}] {self.level}: {self.message}\033[0m"
