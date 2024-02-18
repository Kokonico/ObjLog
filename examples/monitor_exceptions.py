"""log python errors with objlog without extra code"""

from objlog import LogNode, LogMessage
from objlog.LogMessages import Debug, Info, Warn, Error, Fatal
from objlog.utils import monitor

# create a log node
log = LogNode(name="Error Catching Example", print_to_console=True)

# do some logging

log.log(Debug("this is a debug message"))
log.log(Info("this is an info message"))
log.log(Warn("this is a warning message"))
log.log(Error("this is an error message"))

# use the monitor decorator to log any exceptions that occur

# it will log the exception and fail silently
@monitor(log)
def divide_by_zero():
    return 1 / 0

# run the function
divide_by_zero()

# to not fail silently, set raise_exceptions to True

# it will log the exception and raise it

@monitor(log, raise_exceptions=True)
def syntax_error():
    return eval("1 +")

# run the function
syntax_error()
