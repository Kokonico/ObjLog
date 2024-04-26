"""The LogNode class, the main class of the ObjLogger"""
from objlog.Base.LogMessage import LogMessage  # "no parent package" error happens when I don't specify the package,
# IDK why
from objlog.LogMessages import Debug, Error, Fatal, PythonExceptionMessage

from typing import TypeVar, Type, Union

LogMessageType = TypeVar('LogMessageType', bound=LogMessage)

from collections import deque


class LogNode:
    """
    A LogNode, the main class of the ObjLogger.
    It can log messages to a file, to the console, or both.

    :param name: The name of the LogNode.
    :param log_file: The file to log to, if None, the LogNode will not log to a file.
    :param print_to_console: Whether to print messages to the console, if False, the LogNode will not print messages.
    :param print_filter: A list of LogMessage types to filter the messages to be printed to the console.
    :param max_messages_in_memory: The maximum number of messages to be saved in memory, defaults to 500.
    :param max_log_messages: The maximum number of messages to be saved in the log file, defaults to 1000.
    :param log_when_closed: Whether to log a message when the LogNode is deleted.
    :param wipe_log_file_on_init: Whether to clear the log file specified (if any) when the LogNode is created.
    """

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
        if log_file:
            with self.open(log_file) as f:
                self.log_len = len(f.readlines())
                if self.log_len > max_log_messages:
                    # chop the file
                    lines = f.readlines()
                    lines = lines[-max_log_messages:]
                    with self.open(log_file, "w") as f2:
                        f2.writelines(lines)
        else:
            self.log_len = 0

        # check if log exists (in the file system), and if so, clear it
        if isinstance(log_file, str) and wipe_log_file_on_init:
            # your IDE might say that this code is broken, but it's not.
            # i'm aware that it should probably be lit on fire and thrown into a volcano, but it works for now.
            with self.open(log_file, "w+") as f:
                f.write("")

    # noinspection PyUnresolvedReferences
    def log(self, message: LogMessage | Exception | BaseException, override_log_file: str | None = None,
            force_print: tuple[bool, bool] = (False, False),
            preserve_message_in_memory: bool = True) -> None:
        """
        Logs a message to the LogNode.

        :param message: The message to log
        :param override_log_file:  overrides the log file to log to set in the LogNode.
        :param force_print: Force the message to either print or not print, regardless of the LogNode's print setting.
        :param preserve_message_in_memory: Weather to save the message in the LogNode's memory.
        :return: None
        """
        # make sure it's a LogMessage or its subclass
        if not isinstance(message, LogMessage) and not isinstance(message, Exception) and not isinstance(message,
                                                                                                         BaseException):
            raise TypeError("message must be a LogMessage/Exception or its subclass")
        else:
            if isinstance(message, Exception):
                message = PythonExceptionMessage(message)
        if preserve_message_in_memory:
            self.messages.append(message)

        if isinstance(self.log_file, str) or isinstance(override_log_file, str):
            message_str = f"[{self.name}] {str(message)}"

            # log it
            with self.open(self.log_file, "a+") as f:
                # move the file pointer to the beginning of the file
                f.seek(0)

                # check if the number of messages in the file is bigger than/equal to the max
                if self.log_len > self.maxinf:
                    # if so, crop the file's oldest messages recursively until it's smaller than (or equal to) the max
                    lines = f.readlines()
                    lines = lines[-self.maxinf + 1:]  # scuffed code, do not touch
                    with self.open(self.log_file, "w") as f2:
                        f2.writelines(lines)
                    self.log_len = len(lines)

                # write the message
                f.write(message_str + '\n')
                self.log_len += 1
        
        # TODO: fix the force_print thing when passing in an Exception or BaseException
        # we don't need to do this for now, but it's a good idea to do it in the future
        if (self.print or force_print[0]) and (
                self.print_filter is None or isinstance(message, tuple(self.print_filter))):
            if force_print[1] and force_print[0]:
                print(f"[{self.name}] {message.colored()}")
            elif force_print[0] is False and self.print:
                print(f"[{self.name}] {message.colored()}")

    def set_output_file(self, file: str | None, preserve_old_messages: bool = False) -> None:
        """
        Set log output file.
        If preserve_old_messages is True, the old messages will be logged to the new file.

        :param file: The file to log to.
        :param preserve_old_messages: Whether to bring already logged messages to the new file.
        :return: None
        """
        if self.log_file == file:
            return  # if the file is the same, do nothing

        self.log_file = file
        if preserve_old_messages and isinstance(file, str):
            for i in self.messages:
                self.log(i, preserve_message_in_memory=False, override_log_file=file, force_print=(True, False))

    def dump_messages(self, file: str, elementfilter: list | None = None,
                      wipe_messages_from_memory: bool = False) -> None:
        """
        Dump all logged messages to a file, also filtering them if needed.

        :param file: The file to dump the messages to.
        :param elementfilter: A list of LogMessage types to filter the messages to be dumped.
        :param wipe_messages_from_memory: Whether to wipe the messages from the LogNode's memory after dumping them.
        :return: None
        """
        if elementfilter is not None:
            with self.open(file, "a") as f:
                for i in self.messages:
                    if isinstance(i, tuple(elementfilter)):
                        f.write(str(i) + '\n')
        else:
            with self.open(file, "a") as f:
                f.write('\n'.join(map(str, self.messages)))
        if wipe_messages_from_memory:
            self.wipe_messages()

    def filter(self, typefilter: list[Union[Type[LogMessage], Type[Exception], Type[BaseException]]], filter_logfiles: bool = False) -> None:
        """
        Filter messages saved in memory, optionally the logfiles too.

        :param typefilter: A list of LogMessage types to filter the messages saved in memory.
        :param filter_logfiles: Whether to filter the log files too.
        :return: None
        """
        self.messages = self.get(*typefilter)
        if filter_logfiles:
            if isinstance(self.log_file, str):
                with self.open(self.log_file, "w") as f:
                    for i in self.messages:
                        f.write(str(i) + '\n')

    def dump_messages_to_console(self, *elementfilter: Union[
        Type[LogMessage], Type[Exception], Type[BaseException], Type[None]]
                                 ) -> None:
        """
        Dump all logged messages to the console, also filtering them if needed.

        :param elementfilter: A list of LogMessage types to filter the messages to be dumped to the console.
        :return: None
        """

        for i in self.messages:
            if elementfilter is None or (elementfilter is not None and isinstance(i, tuple(elementfilter))):
                self.log(i, force_print=(True, True), preserve_message_in_memory=False)

    def wipe_messages(self, wipe_logfiles: bool = False) -> None:
        """
        Wipe all messages from memory, can free up a lot of memory if you have a lot of messages,
         but you won't be able to dump the previous messages to a file.

        :param wipe_logfiles: Whether to wipe the log files too.
        :return: None
         """
        self.messages = []
        if wipe_logfiles:
            self.clear_log()

    def clear_log(self) -> None:
        """
        Clear the log file.
        WARNING: This will delete all messages saved in the log file.

        :return: None
        """
        if isinstance(self.log_file, str):
            with self.open(self.log_file, "w") as f:
                f.write("")
                self.log_len = 0

    def set_max_messages_in_memory(self, max_messages: int) -> None:
        """
        Set the maximum number of messages to be saved in memory.
        WARNING: This will delete the oldest messages if the new maximum is smaller than the current number of messages.

        :param max_messages: The maximum number of messages to be saved in memory.
        :return: None
        """
        self.max = max_messages
        self.messages = deque(self.messages, maxlen=self.max)

    def set_max_messages_in_log(self, max_file_size: int) -> None:
        """
        Set the maximum message limit of the log file.
        WARNING: This will delete the oldest messages if the new maximum is smaller than the current number of messages.

        :param max_file_size: The maximum number of messages to be saved in the log file.
        :return: None
        """
        self.maxinf = max_file_size
        # crop the file if it's too big
        if isinstance(self.log_file, str):
            with self.open(self.log_file, "r+") as f:
                if self.log_len >= self.maxinf:
                    lines = f.readlines()
                    lines = lines[-self.maxinf:]
                    f.seek(0)
                    f.truncate()
                    f.writelines(lines)
                    self.log_len = len(lines)

    def get(self, *element_filter: Union[Type[LogMessage], Type[Exception], Type[BaseException]] | tuple) -> list:
        """
        Get all messages saved in memory, optionally filtered.

        :param element_filter: A list of LogMessage types to filter the messages to be returned.
        :return: A list of messages saved in memory, optionally filtered.
        """
        if len(element_filter) == 0:
            return list(self.messages)
        else:
            # return list(filter(lambda x: isinstance(x, element_filter), self.messages))
            filtered_messages = []
            for msg in self.messages:
                if isinstance(msg, PythonExceptionMessage):
                    if isinstance(msg.exception, element_filter) or isinstance(msg, element_filter):
                        filtered_messages.append(msg)
                elif isinstance(msg, element_filter):
                    filtered_messages.append(msg)
            return filtered_messages

    def combine(self, other: 'LogNode', merge_log_files: bool = True) -> None:
        """
        Combine two LogNodes, optionally merging their log files.
        Both LogNodes logged messages will be saved in the first LogNode.
        It will modify the first LogNode in place.

        :param other: The other LogNode to combine with.
        :param merge_log_files: Whether to merge the log files of the LogNodes.
        :return: None
        """
        self.messages.extend(other.messages)

        if merge_log_files:
            self.clear_log()
            with self.open(self.log_file, "w") as f:
                for i in self.messages:
                    f.write(str(i) + '\n')

    def squash(self, message: LogMessage, squash_logfile: bool = True) -> None:
        """
        Squash the lognode, i.e., replace all messages with a single message.

        :param message: The message to replace all messages with.
        :param squash_logfile: Whether to squash the log file too.
        """
        self.messages.clear()
        self.messages.append(message)
        if squash_logfile:
            self.clear_log()
            with self.open(self.log_file, "w") as f:
                f.write(str(message) + '\n')

    def has_errors(self) -> bool:
        """
        Check if the log node has any errors (Error, Fatal, PythonExceptionMessage).

        :return: True if the log node has any errors, False otherwise
        """
        return len(self.get(Error, Fatal, PythonExceptionMessage)) > 0

    def has(self, *args: Union[Type[LogMessage], Type[Exception], Type[BaseException]]) -> bool:
        """
        Check if the log node has any of the specified LogMessage types

        :param args: The LogMessage types to check for
        :return: True if the log node has any of the specified LogMessage types, False otherwise
        """
        # ignore the warning, it's a false positive
        return len(self.get(args)) > 0

    def rename(self, new_name: str):
        """
        Rename the LogNode.

        :param new_name: The new name of the LogNode.
        :return: None
        """
        self.name = new_name

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
