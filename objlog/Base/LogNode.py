from objlog.LogMessages import Debug
from .LogMessage import LogMessage


class LogNode:
    """the ObjLogger"""

    def __init__(self, name: str, log_file: str | None = None, print_to_console: bool = False,
                 print_filter: list | None = None, max_messages_in_memory: int = 500, max_log_messages: int = 1000,
                 log_when_closed: bool = True):
        self.log_file = log_file
        self.name = name
        self.print = print_to_console
        self.messages = []
        self.max = max_messages_in_memory
        self.maxinf = max_log_messages
        self.print_filter = print_filter
        self.log_closure_message = log_when_closed

    def log(self, message, override_log_file: str | None = None, force_print: tuple[bool, bool] = (False, False),
            preserve_message_in_memory: bool = True) -> None:
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

    def set_output_file(self, file: str | None, preserve_old_messages: bool = False) -> None:
        """set log output file."""
        if self.log_file == file:
            return  # if the file is the same, do nothing

        self.log_file = file
        if preserve_old_messages and isinstance(file, str):
            for i in self.messages:
                self.log(i, preserve_message_in_memory=False, override_log_file=file, force_print=(True, False))

    def dump_messages(self, file: str, elementfilter: list | None = None, wipe_messages_from_memory: bool = False) -> None:
        """dump all logged messages to a file, also filtering them if needed"""
        with open(file, "a") as f:
            for i in self.messages:
                if elementfilter is None or (elementfilter is not None and isinstance(i, tuple(elementfilter))):
                    f.write(str(i) + '\n')
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

    def set_max_messages_in_memory(self, max_messages: int) -> None:
        """set the maximum amount of messages to be saved in memory"""
        self.max = max_messages
        # crop the list if it's too big
        if len(self.messages) > self.max:
            self.messages = self.messages[-self.max:]

    def set_max_messages_in_log(self, max_file_size: int) -> None:
        """set the maximum message limit of the log file"""
        self.maxinf = max_file_size
        # crop the file if it's too big
        if isinstance(self.log_file, str):
            with open(self.log_file, "r+") as f:
                lines = f.readlines()
                if len(lines) > self.maxinf:
                    lines = lines[-self.maxinf:]
                    f.seek(0)
                    f.truncate()
                    f.writelines(lines)

    def get(self, element_filter: list | None) -> list:
        """get all messages saved in memory, optionally filtered"""
        if element_filter is None:
            return self.messages
        else:
            return list(filter(lambda x: isinstance(x, tuple(element_filter)), self.messages))

    def __repr__(self):
        return f"LogNode {self.name} at output {self.log_file}"

    def __len__(self):
        return len(self.messages)

    def __del__(self):
        # log the deletion
        if self.log_closure_message:
            self.log(Debug("LogNode closed."))
        # do the actual deletion
        del self
