"""more ways to monitor exceptions"""

from objlog import LogNode, utils
from objlog.LogMessages import Debug, Info, Warn, Error

# create a log node

log = LogNode(name="Error Catching Example", print_to_console=True)

# do some logging

log.log(Debug("this is a debug message"))
log.log(Info("this is an info message"))
log.log(Warn("this is a warning message"))
log.log(Error("this is an error message"))


# use the monitor decorator to log any exceptions that occur, and fail semi-silently

# This is recommended for user-facing code, as it will log the exception and its location. However, it will not
# provide a stack trace on the user's console for internal code

# this is not recommended for internal code, as it will fail silently, and the exception will not be raised
# (meaning you cannot catch it)

# it will print the error and its message if the log node does not print to the console,
# and will provide a stack trace if the log node does not print to the console or save to a file

# keep in mind that raise_exceptions is overridden by exit_on_exception,
# and will not be used if exit_on_exception is set to True

# So @monitor(log, exit_on_exception=True)
# is equivalent to both
# @monitor(log, exit_on_exception=True, raise_exceptions=True)
# and
# @monitor(log, exit_on_exception=True, raise_exceptions=False)

@utils.monitor(log, exit_on_exception=True)
def divide_by_zero():
    return 1 / 0


# run the function
# this will fail semi-silently, as the exception will be logged, and the program will close.
# however, no message will be printed to the console, as the log node prints to the console


divide_by_zero()
