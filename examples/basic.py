"""A basic example of using ObjLog"""
from objlog import LogNode
from objlog.LogMessages import Debug, Info, Warn, Error, Fatal

# create log node
log = LogNode(name="Basic Example", print_to_console=True)

# log some messages

log.log(Debug("This is a debug message"))
log.log(Info("This is an info message"))
log.log(Warn("This is a warning message"))
log.log(Error("This is an error message"))
log.log(Fatal("This is a fatal message"))

# delete log node
del log
