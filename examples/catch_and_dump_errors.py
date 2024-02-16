"""example about catching errors and dumping them"""

from objlog import LogNode, LogMessage
from objlog.LogMessages import Debug, Info, Warn, Error, Fatal

# create a log node

log = LogNode(name="Error Catching Example")

# do some logging

log.log(Debug("this is a debug message"))
log.log(Info("this is an info message"))
log.log(Warn("this is a warning message"))
log.log(Error("this is an error message"))
log.log(Fatal("this is a fatal message"))

# catch and dump errors

if log.has_errors():
    print("caught an error, dumping...")
    log.dump_messages("errors.log", [Error, Fatal])

# custom error handling

log = LogNode(name="Custom Error Handling Example")

log.log(Debug("this is a debug message"))

# custom error

class CustomError(LogMessage):
    level = "CUSTOM ERROR"
    color = "\033[1;35m"


log.log(CustomError("this is a custom error message"))

if log.has(CustomError):
    print("caught a custom error, dumping...")
    log.dump_messages("custom_errors.log", [CustomError])
