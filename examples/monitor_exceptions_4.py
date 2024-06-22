"""even more exceptions to monitor"""

from objlog import LogNode, LogMessage, utils
from objlog.LogMessages import Debug, Info, Warn, Error, Fatal

# create a log node

log = LogNode(name="Error Catching Example", log_file="error.log")


# this log node will not print to the console and save its log messages to a file

# by default, the log node will not print to the console, and will not save it to a file

# so this will print the error and its message, and will not provide a stack trace

# the location of the error will be logged, but the stack trace will not be printed

@utils.monitor(log, exit_on_exception=True)
def type_error():
    # noinspection PyTypeChecker
    return 1 + "1"


# run the function, this will log the exception, print the error, and close the program

type_error()
