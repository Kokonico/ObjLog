"""the juicy internals of ObjLog"""
from datetime import datetime
from time import time_ns


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

    def __str__(self):
        return f"[{self.timestamp}] {self.level}: {self.message}"

    def __repr__(self):
        return f"{self.level}: {self.message}"

    def __eq__(self, other):
        return self.level == other.level and self.message == other.message and self.timestamp == other.timestamp

    def colored(self):
        """return a colored version of the message"""
        return f"{self.color}[{self.timestamp}] {self.level}: {self.message}\033[0m"


class LogNode:
    """the ObjLogger"""

    def __init__(self, name: str, log_file: str | None = None, print_to_console: bool = False, print_filter: list | None = None, max_messages_in_memory: int = 500, max_file_size: int = 200):
        self.log_file = log_file
        self.name = name
        self.print = print_to_console
        self.messages = []
        self.max = max_messages_in_memory
        self.maxinf = max_file_size
        self.print_filter = print_filter

    def log(self, message, override_log_file: str | None = None, force_print: tuple[bool, bool] = (False, False),
            preserve_message_in_memory: bool = True):
        """log a message"""
        # make sure it's a LogMessage or its subclass
        if not isinstance(message, LogMessage):
            raise TypeError("message must be a LogMessage or its subclass")
        if preserve_message_in_memory:
            if len(self.messages) < self.max:
                self.messages.append(message)
            else:
                self.messages.pop(0)
                self.messages.append(message)  # remove the first message and add the new one


        if isinstance(self.log_file, str) or isinstance(override_log_file, str):
            message_str = f"[{self.name}] {str(message)}"
            
            # log it
            with open(self.log_file, "a+") if override_log_file is None else open(override_log_file, "a") as f:
                # move the file pointer to the beginning of the file
                f.seek(0)
                
                # check if the amount of messages in the file is bigger than/equal to the max
                lines = f.readlines()
                if len(lines) >= self.maxinf:
                    # get the first line
                    lines.pop(0)
                    # move the file pointer to the beginning of the file before writing
                    f.seek(0)
                    # truncate the file to remove its content
                    f.truncate()
                    # remove the last line (it's empty)
                    lines.pop()
                    # write the lines back
                    f.writelines(lines)
                
                # write the message
                f.write(message_str + '\n')






        if (self.print or force_print[0]) and (
                self.print_filter is None or isinstance(message, tuple(self.print_filter))):
            if force_print[1] and force_print[0]:
                print(f"[{self.name}] {message.colored()}")
            elif force_print[0] is False and self.print:
                print(f"[{self.name}] {message.colored()}")

    def set_output_file(self, file: str | None, preserve_old_messages: bool = False):
        """set log output file."""
        if self.log_file == file:
            return  # if the file is the same, do nothing

        self.log_file = file
        if preserve_old_messages and isinstance(file, str):
            for i in self.messages:
                self.log(i, preserve_message_in_memory=False, override_log_file=file, force_print=(True, False))

    def dump_messages(self, file: str, elementfilter: list | None = None, wipe_messages_from_memory: bool = False):
        """dump all logged messages to a file, also filtering them if needed"""
        with open(file, "a") as f:
            for i in self.messages:
                if elementfilter is None or (elementfilter is not None and isinstance(i, tuple(elementfilter))):
                    f.write(str(i) + '\n')
        if wipe_messages_from_memory:
            self.wipe_messages()

    def filter(self, typefilter: list, filter_logfiles: bool = False):
        """filter messages saved in memory, optionally the logfiles too"""
        self.messages = list(filter(lambda x: isinstance(x, tuple(typefilter)), self.messages))
        if filter_logfiles:
            if isinstance(self.log_file, str):
                with open(self.log_file, "w") as f:
                    for i in self.messages:
                        f.write(str(i) + '\n')

    def dump_messages_to_console(self, elementfilter: list | None = None):
        """dump all logged messages to the console, also filtering them if needed"""
        for i in self.messages:
            if elementfilter is None or (elementfilter is not None and isinstance(i, tuple(elementfilter))):
                self.log(i, force_print=(True, True), preserve_message_in_memory=False)

    def wipe_messages(self, wipe_logfiles: bool = False):
        """wipe all messages from memory, can free up a lot of memory if you have a lot of messages,
         but you won't be able to dump the previous messages to a file"""
        self.messages = []
        if wipe_logfiles:
            self.clear_log()

    def clear_log(self):
        """clear the log file"""
        if isinstance(self.log_file, str):
            with open(self.log_file, "w") as f:
                f.write("")

    def set_max_messages_in_memory(self, max_messages: int):
        """set the maximum amount of messages to be saved in memory"""
        self.max = max_messages
    
    def set_max_file_size(self, max_file_size: int):
        """set the maximum size of the log file"""
        self.maxinf = max_file_size

    def __repr__(self):
        return f"LogNode {self.name} at output {self.log_file}"
