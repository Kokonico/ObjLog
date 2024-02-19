"""even more exceptions to monitor"""

from objlog import LogNode, LogMessage, utils
from objlog.LogMessages import Debug, Info, Warn, Error, Fatal

# create a log node

log = LogNode(name="Error Catching Example")

# this log node will not print to the console

# by default, the log node will not print to the console, and will not save it to a file

# so this will print the error and its message, and will provide a stack trace

@utils.monitor(log, exit_on_exception=True)
def type_error():
    # noinspection PyTypeChecker
    return 1 + "1"

# run the function, this will log the exception, print the error and the stacktrace, and close the program

type_error()
