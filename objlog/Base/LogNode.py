"""The LogNode class, the main class of the ObjLogger"""
from objlog.Base.LogMessage import LogMessage  # "no parent package" error happens when I don't specify the package,
# IDK why
from objlog.LogMessages import Debug, Info, Warn, Error, Fatal, _PythonExceptionMessage
import objlog

from typing import TypeVar, Type

LogMessageType = TypeVar('LogMessageType', bound=LogMessage)

from collections import deque

import sys, traceback

# TODO: putting any python exceptions in filter lists will not filter them (any function with one), pls fix before 2.0
# TODO: same with get() and has(), putting any python exceptions in the filter list will not detect/return them.


class LogNode:
    """A LogNode, the main class of the ObjLogger. It can log messages to a file, to the console, or both."""

    open = open  # this prevents an exception from being raised when the LogNode is deleted, not sure why

    def __init__(self, name: str, log_file: str | None = None, print_to_console: bool = False,
                 print_filter: list | None = None, max_messages_in_memory: int = 500, max_log_messages: int = 1000,
                 log_when_closed: bool = True, wipe_log_file_on_init: bool = False):
        self.log_file = log_file
        self.name = name
        self.print = print_to_console
        self.messages = deque(maxlen=max_messages_in_memory)
        self.max = max_messages_in_memory
        self.maxinf = max_log_messages
        self.print_filter = print_filter
        self.log_closure_message = log_when_closed
        self.log_len = 0

        # check if log exists (in the file system), and if so, clear it
        if isinstance(log_file, str) and wipe_log_file_on_init:
            with open(log_file, "w+") as f:
                f.write("")

    def log(self, message, override_log_file: str | None = None, force_print: tuple[bool, bool] = (False, False),
            preserve_message_in_memory: bool = True) -> None:
        """log a message"""
        # make sure it's a LogMessage or its subclass
        if not isinstance(message, LogMessage) and not isinstance(message, Exception) and not isinstance(message, BaseException):
            raise TypeError("message must be a LogMessage/Exception or its subclass")
        else:
            if isinstance(message, Exception):
                message = _PythonExceptionMessage(message)
        if preserve_message_in_memory:
            self.messages.append(message)

        if isinstance(self.log_file, str) or isinstance(override_log_file, str):
            message_str = f"[{self.name}] {str(message)}"

            # log it
            with open(self.log_file, "a+") as f:
                # move the file pointer to the beginning of the file
                f.seek(0)

                # check if the number of messages in the file is bigger than/equal to the max
                if self.log_len > self.maxinf:
                    # if so, crop the file's oldest messages recursively until it's smaller than (or equal to) the max
                    lines = f.readlines()
                    lines = lines[-self.maxinf + 1:]  # scuffed code, do not touch
                    with open(self.log_file, "w") as f2:
                        f2.writelines(lines)
                    self.log_len = len(lines)

                # write the message
                f.write(message_str + '\n')
                self.log_len += 1

        if (self.print or force_print[0]) and (
                self.print_filter is None or isinstance(message, tuple(self.print_filter))):
            if force_print[1] and force_print[0]:
                print(f"[{self.name}] {message.colored()}")
            elif force_print[0] is False and self.print:
                print(f"[{self.name}] {message.colored()}")

    def set_output_file(self, file: str | None, preserve_old_messages: bool = False) -> None:
        """set log output file."""
        if self.log_file == file:
            return  # if the file is the same, do nothing

        self.log_file = file
        if preserve_old_messages and isinstance(file, str):
            for i in self.messages:
                self.log(i, preserve_message_in_memory=False, override_log_file=file, force_print=(True, False))

    def dump_messages(self, file: str, elementfilter: list | None = None,
                      wipe_messages_from_memory: bool = False) -> None:
        """dump all logged messages to a file, also filtering them if needed"""
        if elementfilter is not None:
            with open(file, "a") as f:
                for i in self.messages:
                    if isinstance(i, tuple(elementfilter)):
                        f.write(str(i) + '\n')
        else:
            with open(file, "a") as f:
                f.write('\n'.join(map(str, self.messages)))
        if wipe_messages_from_memory:
            self.wipe_messages()

    def filter(self, typefilter: list, filter_logfiles: bool = False) -> None:
        """filter messages saved in memory, optionally the logfiles too"""
        self.messages = list(filter(lambda x: isinstance(x, tuple(typefilter)), self.messages))
        if filter_logfiles:
            if isinstance(self.log_file, str):
                with open(self.log_file, "w") as f:
                    for i in self.messages:
                        f.write(str(i) + '\n')

    def dump_messages_to_console(self, elementfilter: list | None = None) -> None:
        """dump all logged messages to the console, also filtering them if needed"""
        for i in self.messages:
            if elementfilter is None or (elementfilter is not None and isinstance(i, tuple(elementfilter))):
                self.log(i, force_print=(True, True), preserve_message_in_memory=False)

    def wipe_messages(self, wipe_logfiles: bool = False) -> None:
        """wipe all messages from memory, can free up a lot of memory if you have a lot of messages,
         but you won't be able to dump the previous messages to a file"""
        self.messages = []
        if wipe_logfiles:
            self.clear_log()

    def clear_log(self) -> None:
        """clear the log file"""
        if isinstance(self.log_file, str):
            with open(self.log_file, "w") as f:
                f.write("")
                self.log_len = 0

    def set_max_messages_in_memory(self, max_messages: int) -> None:
        """set the maximum number of messages to be saved in memory"""
        self.max = max_messages
        self.messages = deque(self.messages, maxlen=self.max)

    def set_max_messages_in_log(self, max_file_size: int) -> None:
        """set the maximum message limit of the log file"""
        self.maxinf = max_file_size
        # crop the file if it's too big
        if isinstance(self.log_file, str):
            with open(self.log_file, "r+") as f:
                if self.log_len >= self.maxinf:
                    lines = f.readlines()
                    lines = lines[-self.maxinf:]
                    f.seek(0)
                    f.truncate()
                    f.writelines(lines)
                    self.log_len = len(lines)

    def get(self, element_filter: list | None = None) -> list:
        """get all messages saved in memory, optionally filtered"""
        if element_filter is None:
            return list(self.messages)
        else:
            return list(filter(lambda x: isinstance(x, tuple(element_filter)), self.messages))

    def combine(self, other: 'LogNode', merge_log_files: bool = True) -> None:
        """combine two LogNodes."""
        self.messages.extend(other.messages)

        if merge_log_files:
            self.clear_log()
            with open(self.log_file, "w") as f:
                for i in self.messages:
                    f.write(str(i) + '\n')

    def squash(self, message: LogMessage) -> None:
        """squash the lognode, i.e., replace all messages with a single message"""
        self.messages.clear()
        self.messages.append(message)

    def has_errors(self) -> bool:
        """check if the log node has any errors"""
        return len(self.get([Error, Fatal])) > 0

    def has(self, *args: Type[LogMessageType]) -> bool:
        """check if the log node has any of the specified LogMessage types"""
        return len(self.get(list(args))) > 0

    def __repr__(self):
        return f"LogNode {self.name} at output {self.log_file}" if isinstance(self.log_file, str) else \
            f"LogNode {self.name} at output console" if self.print else f"LogNode {self.name} at output None"

    def __len__(self):
        return len(self.messages)

    def __contains__(self, item: LogMessage):
        return item in self.messages

    def __del__(self):
        # log the deletion
        if self.log_closure_message:
            self.log(Debug("LogNode closed."))
        # python will delete self automatically (thanks python)

    def __getitem__(self, item):
        # gets an item from the messages
        return self.messages[item]

    def __iter__(self):
        # iterate over the messages
        return iter(self.messages)
