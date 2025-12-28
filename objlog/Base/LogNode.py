"""The LogNode class, the main class of the ObjLogger"""
from .LogMessage import LogMessage
from ..LogMessages import Debug, Error, Fatal, PythonExceptionMessage
from ..constants import VERSION_MAJOR as LGND_VERSION
from .internal import ObjLogInternalError

from typing import TypeVar, Type, Union, Protocol

LogMessageType = TypeVar('LogMessageType', bound=LogMessage)

import os
from collections import deque
import pickle
import random
import time
# import asyncio
import threading
import sys
import traceback
from queue import Queue


class Loggable(Protocol):
    """
    just for type hinting, don't use this class
    """

    def __init__(self, message: str):
        pass

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
    :param enabled: Whether the LogNode is enabled, if False, the LogNode will not log any messages.
    :param asynchronous: Whether to have the LogNode run asynchronously, offloading a majority of its work to a separate thread.
    Usually faster for logging large amounts of messages.
    However, it can be slower if you aren't logging many messages or only saving them, not printing or logging to a file.
    only minor changes are needed to replace a synchronous LogNode with an asynchronous one.
    Make sure to use `await_finish()` when you need to ensure all messages have been processed.
    Any function that reads from the LogNode (like `get()`) will automatically wait for the LogNode to finish processing.
    """

    open = open  # I removed this once before, and it broke log on quit, so putting it back

    def __init__(self, name: str, log_file: str | None = None, print_to_console: bool = False,
                 print_filter: list | None = None, max_messages_in_memory: int = 500, max_log_messages: int = 1000,
                 log_when_closed: bool = True, wipe_log_file_on_init: bool = False, enabled: bool = True, asynchronous: bool = False):
        self.enabled = enabled
        self.version = LGND_VERSION
        self.log_file = log_file
        self.name = name
        self.print = print_to_console
        self.messages = deque(maxlen=max_messages_in_memory)
        self.max = max_messages_in_memory
        self.maxinf = max_log_messages
        self.print_filter = print_filter
        self.log_when_closed = log_when_closed
        self.uuid = time.time_ns() // random.randint(1, 10000) + random.randint(-25, 25)
        self._asynchronous = asynchronous
        self.log_len = 0

        self._lock = threading.Lock()

        self.command_queue = Queue()
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        if self._asynchronous:
            self.worker_thread.start()


        if log_file:
            # create the log file if it doesn't exist
            if not os.path.exists(log_file) or wipe_log_file_on_init:
                with open(log_file, "w") as f:
                    f.write("")
                self.log_len = 0
            else:
                with open(log_file, 'r') as f:
                    lines = f.readlines()
                if self.log_len > max_log_messages:
                    lines = lines[-max_log_messages:]
                    with open(log_file, "w+") as f:
                        if wipe_log_file_on_init:
                            f.write("")
                            self.log_len = 0
                        else:
                            f.writelines(lines)
                self.log_len = len(lines)
        else:
            self.log_len = 0

    def log(self, *messages: LogMessageType | Exception | BaseException,
            override_log_file: str | None = None,
            force_print: tuple[bool, bool] = (False, False),
            preserve_message_in_memory: bool = True,
            verbose: bool = False, _bypass_async: bool = False
            ) -> None | dict:
        """
        Logs a message to the LogNode. Does nothing if the LogNode is disabled.

        :param messages: The message(s) to log
        :param override_log_file:  overrides the log file to log to set in the LogNode.
        :param force_print: Force the message to either print or not print, regardless of the LogNode's print setting.
        :param preserve_message_in_memory: Weather to save the message in the LogNode's memory.
        :param verbose: Gives you a list of some stats about the log, like how long it took to log, the object itself, etc. WILL DISABLE ASYNC LOGGING ON THIS CALL.
        :param _bypass_async: Internal use only, bypasses the asynchronous logging system if enabled.
        :return: None | dict
        """

        if self.asynchronous and not _bypass_async and not verbose:
            # add the log command to the queue
            # _bypass_async is set within the worker thread to avoid infinite loop
            self.command_queue.put((self.log, messages, {
                "override_log_file": override_log_file,
                "force_print": force_print,
                "preserve_message_in_memory": preserve_message_in_memory,
                "verbose": verbose,
            }))
            return None

        if not self.enabled:
            return None

        if verbose:
            verbose_out = {
                "processtime_ns": 0,
                "logged": []
            }

        if verbose:
            log_start = time.time_ns()

        # convert all exceptions to PythonExceptionMessage
        for i in range(len(messages)):
            if not isinstance(messages[i], LogMessage) and not isinstance(messages[i], Exception) and not isinstance(messages[i],
                                                                                                             BaseException):
                raise TypeError("message must be a LogMessage/Exception or its subclass")

            if isinstance(messages[i], (BaseException, Exception)):
                messages = list(messages)
                messages[i] = PythonExceptionMessage(messages[i])

        for i, message in enumerate(messages):
            if verbose:
                current_verbose = {"message": message.message, "id_in_node": -1000, "type": message.level}

                if preserve_message_in_memory:
                    current_verbose["id_in_node"] = len(self.messages) + i + 1
                else:
                    current_verbose["id_in_node"] = -1001

            if (self.print or force_print[0]) and (
                    self.print_filter is None or isinstance(message, tuple(self.print_filter))):
                if force_print[1] or self.print:
                    # print(f"[{self.name}] {message.colored()}")
                    sys.stdout.write(f"[{self.name}] {message.colored()}\n") # MUCH FASTER!
            if verbose:
                # note: verbose_out && current_verbose will always exist if verbose is True
                # noinspection PyUnboundLocalVariable
                verbose_out["logged"].append(current_verbose)

        if preserve_message_in_memory:
            self.messages.extend(messages)

        if verbose:
            log_end = time.time_ns()
            # that warning is a false positive trust
            # noinspection PyUnboundLocalVariable
            verbose_out["processtime_ns"] = (log_end - log_start)

        target = self.log_file if not override_log_file else override_log_file

        if isinstance(target, str):

            # ensure the directory exists
            if not os.path.dirname(target) == "":
                os.makedirs(os.path.dirname(target), exist_ok=True)

            # ensure the file exists
            if not os.path.exists(target):
                with self.open(target, "w") as f:
                    f.write("\n".join([f"[{self.name}] {str(message)}" for message in messages]) + "\n")
                    self.log_len = 0

            else:
                # log it
                with self.open(target, "a") as f:
                    f.write("\n".join([f"[{self.name}] {str(message)}" for message in messages]) + "\n")

            self.log_len += len(messages)

            # check if we need to crop the file
            if self.log_len > self.maxinf:
                with self.open(target, "r+") as f:
                    lines = f.readlines()
                    lines = lines[-self.maxinf:]
                    f.seek(0)
                    f.truncate()
                    f.writelines(lines)
                    self.log_len = len(lines)

        return verbose_out if verbose else None

    def set_output_file(self, file: str | None, preserve_old_messages: bool = False, _bypass_async: bool = False) -> None:
        """
        Set log output file.
        If preserve_old_messages is True, the old messages will be logged to the new file.

        :param file: The file to log to.
        :param preserve_old_messages: Whether to bring already logged messages to the new file.
        :param _bypass_async: Internal use only, bypasses async logging system if enabled.
        :return: None
        """
        if self.log_file == file:
            return  # if the file is the same, do nothing

        # check for async logging
        if self.asynchronous and not _bypass_async:
            # add to the command queue
            self.command_queue.put((self.set_output_file, (file, preserve_old_messages), {}))
            return

        self.log_file = file
        if preserve_old_messages and isinstance(file, str):
            self.log(*self.messages, preserve_message_in_memory=False, override_log_file=file, force_print=(True, False), _bypass_async=True)

    def dump_messages(self, file: str, *elementfilter: Union[Type[LogMessage], Type[Exception], Type[BaseException]],
                      wipe_messages_from_memory: bool = False) -> None:
        """
        Dump all logged messages to a file, also filtering them if needed.
        Will wait until the LogNode is not busy if asynchronous logging is enabled.

        :param file: The file to dump the messages to.
        :param elementfilter: A list of LogMessage types to filter the messages to be dumped.
        :param wipe_messages_from_memory: Whether to wipe the messages from the LogNode's memory after dumping them.
        :return: None
        """

        self.await_finish()

        if len(elementfilter) > 0:
            with open(file, "a") as f:
                for i in self.messages:
                    if isinstance(i, elementfilter):
                        f.write(str(i) + '\n')
        else:
            with open(file, "a") as f:
                f.write('\n'.join(map(str, self.messages)))
        if wipe_messages_from_memory:
            self.wipe_messages()

    def filter(self, *typefilter: Union[Type[LogMessage], Type[Exception], Type[BaseException]],
               filter_logfiles: bool = False, _bypass_async: bool = False) -> None:
        """
        Filter messages saved in memory, optionally the logfiles too.

        :param typefilter: A list of LogMessage types to filter the messages saved in memory.
        :param filter_logfiles: Whether to filter the log files too.
        :param _bypass_async: Internal use only, bypasses async logging system if enabled.
        :return: None
        """

        if self.asynchronous and not _bypass_async:
            # add to the command queue
            self.command_queue.put((self.filter, typefilter, {
                "filter_logfiles": filter_logfiles
            }))
            return

        self.messages = deque(self.get(*typefilter, _bypass_await_finish=True), maxlen=self.max)
        if filter_logfiles:
            if isinstance(self.log_file, str):
                with open(self.log_file, "w") as f:
                    for i in self.messages:
                        f.write(str(i) + '\n')

    def dump_messages_to_console(self, *elementfilter: Union[
        Type[LogMessage], Type[Exception], Type[BaseException], Type[None]]
                                 ) -> None:
        """
        Dump all logged messages to the console, also filtering them if needed.
        Blocks until LogNode is no longer busy if asynchronous logging is enabled.

        :param elementfilter: A list of LogMessage types to filter the messages to be dumped to the console.
        :return: None
        """

        self.await_finish()

        for i in self.messages:
            if elementfilter is None or elementfilter == (None,):
                print(i.colored())
            elif isinstance(i, tuple(elementfilter)):
                print(i.colored())
            elif tuple(elementfilter) == ():
                print(i.colored())

    def wipe_messages(self, wipe_logfiles: bool = False, _bypass_async: bool = False) -> None:
        """
        Wipe all messages from memory, can free up a lot of memory if you have a lot of messages,
         but you won't be able to dump the previous messages to a file.

        :param wipe_logfiles: Whether to wipe the log files too.
        :param _bypass_async: Internal use only, bypasses async logging system if enabled.
        :return: None
         """

        if self.asynchronous and not _bypass_async:
            # add to the command queue
            self.command_queue.put((self.wipe_messages, (), {
                "wipe_logfiles": wipe_logfiles
            }))
            return

        self.messages = deque(maxlen=self.max)
        if wipe_logfiles:
            self.clear_log(_bypass_async=True)

    def clear_log(self, _bypass_async: bool = False) -> None:
        """
        Clear the log file.
        WARNING: This will delete all messages saved in the log file.

        :return: None
        """

        if self.asynchronous and not _bypass_async:
            # add to the command queue
            self.command_queue.put((self.clear_log, (), {}))
            return

        if isinstance(self.log_file, str):
            with open(self.log_file, "w") as f:
                f.write("")
                self.log_len = 0

    def set_max_messages_in_memory(self, max_messages: int, _bypass_async: bool = False) -> None:
        """
        Set the maximum number of messages to be saved in memory.
        WARNING: This will delete the oldest messages if the new maximum is smaller than the current number of messages.

        :param max_messages: The maximum number of messages to be saved in memory.
        :param _bypass_async: Internal use only, bypasses async logging system if enabled.
        :return: None
        """
        if self.asynchronous and not _bypass_async:
            # add to the command queue
            self.command_queue.put((self.set_max_messages_in_memory, (max_messages,), {}))
            return

        self.max = max_messages
        self.messages = deque(self.messages, maxlen=self.max)

    def set_max_messages_in_log(self, max_file_size: int, _bypass_async: bool = False) -> None:
        """
        Set the maximum message limit of the log file.
        WARNING: This will delete the oldest messages if the new maximum is smaller than the current number of messages.

        :param max_file_size: The maximum number of messages to be saved in the log file.
        :param _bypass_async: Internal use only, bypasses async logging system if enabled.
        :return: None
        """

        if self.asynchronous and not _bypass_async:
            # add to the command queue
            self.command_queue.put((self.set_max_messages_in_log, (max_file_size,), {}))
            return

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

    def get(self, *element_filter: Union[Type[LogMessage], Type[Exception], Type[BaseException]] | tuple, _bypass_await_finish: bool = False) -> list:
        """
        Get all messages saved in memory, optionally filtered.
        Will block until the LogNode is not busy if asynchronous logging is enabled.

        :param element_filter: A list of LogMessage types to filter the messages to be returned.
        :param _bypass_await_finish: Internal use only, bypasses await_finish call. TOGGLING ON WILL RESULT IN UNRELIABLE RESULTS IF ASYNC LOGGING IS ENABLED.
        :return: A list of messages saved in memory, optionally filtered.
        """

        if not _bypass_await_finish:
            self.await_finish()
            self._lock.acquire()

        # looks stupid not using `with`, but it's needed for the bypass flag to work properly

        if len(element_filter) == 0:
            if not _bypass_await_finish:
                self._lock.release()
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
            if not _bypass_await_finish:
                self._lock.release()
            return filtered_messages

    def combine(self, other: 'LogNode', merge_log_files: bool = True, _bypass_async: bool = False) -> None:
        """
        Combine two LogNodes, optionally merging their log files.
        Both LogNodes logged messages will be saved in the first LogNode.
        It will modify the first LogNode in place.

        :param other: The other LogNode to combine with.
        :param merge_log_files: Whether to merge the log files of the LogNodes.
        :param _bypass_async: Internal use only, bypasses async logging system if enabled.
        :return: None
        """

        if self.asynchronous and not _bypass_async:
            # add to the command queue
            self.command_queue.put((self.combine, (other, merge_log_files), {}))
            return

        # ensure the other lognode has finished processing if it's asynchronous
        # note: no need to check if self is asynchronous, as we run within the worker thread if it is, nullifying the need to wait
        other.await_finish()

        with other._lock:
            self.messages.extend(other.messages)
            if merge_log_files:
                self.clear_log(_bypass_async=True)
                with open(self.log_file, "w") as f:
                    for i in self.messages:
                        f.write(str(i) + '\n')

    def squash(self, message: LogMessage, squash_logfile: bool = True, _bypass_async: bool = False) -> None:
        """
        Squash the lognode, i.e., replace all messages with a single message.

        :param message: The message to replace all messages with.
        :param squash_logfile: Whether to squash the log file too.
        :param _bypass_async: Internal use only, bypasses async logging system if enabled.
        """

        if self.asynchronous and not _bypass_async:
            # add to the command queue
            self.command_queue.put((self.squash, (message, squash_logfile), {}))
            return

        self.messages.clear()
        self.messages.append(message)
        if squash_logfile:
            self.clear_log()
            with open(self.log_file, "w") as f:
                f.write(str(message) + '\n')

    def has_errors(self) -> bool:
        """
        Check if the log node has any errors (Error, Fatal, PythonExceptionMessage).
        Will block until the LogNode is not busy if asynchronous logging is enabled.

        :return: True if the log node has any errors, False otherwise
        """
        return self.has(Error, Fatal, PythonExceptionMessage)

    def has(self, *args: Union[Type[LogMessage], Type[Exception], Type[BaseException]]) -> bool:
        """
        Check if the log node has any of the specified LogMessage types
        Will block until the LogNode is not busy if asynchronous logging is enabled.

        :param args: The LogMessage types to check for
        :return: True if the log node has any of the specified LogMessage types, False otherwise
        """
        self.await_finish()
        # ignore the warning, it's a false positive
        return len(self.get(*args)) > 0

    def rename(self, new_name: str, update_in_logs: bool = False, _bypass_async: bool = False) -> None:
        """
        Rename the LogNode.

        :param new_name: The new name of the LogNode.
        :param update_in_logs: Whether to update the name in the log files.
        :param _bypass_async: Internal use only, bypasses async logging system if enabled.
        :return: None
        """

        if self.asynchronous and not _bypass_async:
            # add to the command queue
            self.command_queue.put((self.rename, (new_name, update_in_logs), {}))
            return

        if update_in_logs and isinstance(self.log_file, str):
            with open(self.log_file, "w+") as f:
                # replace the name in the log file
                lines = f.readlines()
                for i in lines:
                    f.write(i.replace(f"[{self.name}]", f"[{new_name}]"))
        self.name = new_name

    def save(self, file: str, _bypass_async: bool = False) -> None:
        """
        Save the LogNode to a file.

        :param file: The filename to save the LogNode to.
        :param _bypass_async: Internal use only, bypasses async logging system if enabled.
        :return: None
        """

        if self.asynchronous and not _bypass_async:
            # add to the command queue
            self.command_queue.put((self.save, (file,), {}))
            return

        with open(file + ".lgnd", "wb") as f:
            # pycharm is dumb
            # noinspection PyTypeChecker
            pickle.dump(self, f)

    def enable(self, _bypass_async: bool = False) -> None:
        """
        Enable the LogNode.
        This is analogous to setting self.enabled = True

        :param _bypass_async: Internal use only, bypasses async logging system if enabled.
        :return: None
        """

        if self.asynchronous and not _bypass_async:
            # add to the command queue
            self.command_queue.put((self.enable, (), {}))
            return

        self.enabled = True

    def disable(self, _bypass_async: bool = False) -> None:
        """
        Disable the LogNode.
        This is analogous to setting self.enabled = False

        :param _bypass_async: Internal use only, bypasses async logging system if enabled.

        :return: None
        """

        if self.asynchronous and not _bypass_async:
            # add to the command queue
            self.command_queue.put((self.disable, (), {}))
            return

        self.enabled = False

    def await_finish(self) -> None:
        """
        Wait for the asynchronous logging to finish processing all commands.
        Only applicable if the LogNode is asynchronous, otherwise does nothing.

        :return: None
        """
        if self.asynchronous:
            self.command_queue.join()

    def busy(self):
        """
        Check if the LogNode is busy processing commands.
        Only applicable if the LogNode is asynchronous, otherwise always returns False.

        :return: True if the LogNode is busy, False otherwise.
        """
        if self.asynchronous:
            return not self.command_queue.empty()
        return False

    # properties
    @property
    def asynchronous(self) -> bool:
        """
        Whether the LogNode is asynchronous.

        :return: True if the LogNode is asynchronous, False otherwise.
        """
        return bool(getattr(self, "_asynchronous", False))

    @asynchronous.setter
    def asynchronous(self, value: bool) -> None:
        """
        Set whether the LogNode is asynchronous.
        WARNING: Changing this property will restart the worker thread if enabling asynchronous logging.

        :param value: True to enable asynchronous logging, False to disable it.
        :return: None
        """
        if value and not self.asynchronous:
            # enable asynchronous logging
            self._asynchronous = True
            self.command_queue = Queue()
            self.worker_thread = threading.Thread(target=self._worker, daemon=True)
            self.worker_thread.start()
        elif not value and self.asynchronous:
            # disable asynchronous logging
            self.await_finish()
            with self._lock:
                self._asynchronous = False
                # stop the worker thread
                self.command_queue.put(None)
                self.command_queue.join()
                self.worker_thread.join(timeout=2.0)
                if self.worker_thread.is_alive():
                    # log a warning that the worker thread didn't stop in time
                    # noinspection PyTypeChecker
                    self.log(ObjLogInternalError("LogNode worker thread did not stop in time when disabling asynchronous logging."), _bypass_async=True) # must bypass async to avoid issues during deletion (worker thread has been stopped)

    # internal methods
    def _worker(self):
        """the worker thread for asynchronous logging, don't touch this!"""
        while True:
            # don't process stuff if locked!
            command = self.command_queue.get()
            try:
                if command is None:
                    break
                # process the command
                # list of tuples (callable, args, kwargs)
                # note: append _bypass_async=True to any function call to avoid infinite loop
                func, args, kwargs = command
                with self._lock:
                    try:
                        func(*args, **kwargs, _bypass_async=True)
                    except Exception as e:
                        self.log(ObjLogInternalError(f"Worker thread failed to process command {func.__name__} with args {args} and kwargs {kwargs}: {e}"), _bypass_async=True, force_print=(True, True))
                        self.log(e, _bypass_async=True, force_print=(True, True))
                        # show traceback
                        self.log(ObjLogInternalError(traceback.format_exc()), _bypass_async=True, force_print=(True, True))
            finally:
                self.command_queue.task_done()

    # pickle support
    def __getstate__(self):
        state = self.__dict__.copy()
        # remove the worker thread and command queue from the state
        if 'worker_thread' in state:
            del state['worker_thread']
        if 'command_queue' in state:
            del state['command_queue']
        if '_lock' in state:
            del state['_lock']
        # convert list to deque for messages if not already
        if not isinstance(state['messages'], deque):
            state['messages'] = deque(state['messages'], maxlen=state['max'])
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self._lock = threading.Lock()
        # recreate the worker thread and command queue if asynchronous
        if self.asynchronous:
            self.command_queue = Queue()
            self.worker_thread = threading.Thread(target=self._worker, daemon=True)
            self.worker_thread.start()

    def __repr__(self):
        return f"LogNode {self.name} at output {self.log_file}" if isinstance(self.log_file, str) else \
            f"LogNode {self.name} at output console" if self.print else f"LogNode {self.name} at output None"

    def __len__(self):
        self.await_finish()
        return len(self.messages)

    def __contains__(self, item: LogMessage):
        self.await_finish()
        return item in self.messages

    def __del__(self):
        # ensure the worker thread is stopped & wrapped up
        if self.asynchronous:
            self.await_finish()
            self.command_queue.put(None)
            self.command_queue.join()
            self.worker_thread.join(timeout=2.0)
            if self.worker_thread.is_alive():
                # log a warning that the worker thread didn't stop in time
                # noinspection PyTypeChecker
                self.log(ObjLogInternalError("LogNode worker thread did not stop in time during deletion."), _bypass_async=True) # must bypass async to avoid issues during deletion (worker thread has been stopped)
        # log the closing message
        if self.log_when_closed:
            # noinspection PyTypeChecker
            self.log(Debug("LogNode closed."), _bypass_async=True) # must bypass async to avoid issues during deletion (worker thread has been stopped)
        # python will delete self automatically (thanks python)

    def __getitem__(self, item):
        # gets an item from the messages
        self.await_finish()
        return self.messages[item]

    def __iter__(self):
        # iterate over the messages
        self.await_finish()
        with self._lock:
            return iter(self.messages)
