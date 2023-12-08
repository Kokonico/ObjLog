"""example of printing messages to the console using ObjLog"""

from objlog import LogNode
from objlog.LogMessages import Debug, Info, Warn, Error, Fatal

# create a log node
log = LogNode(name="Print to Console Example", print_to_console=True)

log.log(Debug("This is a debug message"))
log.log(Info("This is an info message"))
log.log(Warn("This is a warning message"))
log.log(Error("This is an error message"))
log.log(Fatal("This is a fatal error message"))

# filter messages that get printed, but all get saved

del log

log = LogNode(name="Print to Console Example", print_to_console=True, print_filter=[Debug, Info, Warn])

log.log(Debug("This is a debug message"))  # this message will be printed
log.log(Info("This is an info message"))  # this message will be printed
log.log(Warn("This is a warning message"))  # this message will be printed
log.log(Error("This is an error message"))  # this message will not be printed
log.log(Fatal("This is a fatal error message"))  # this message will not be printed

log.dump_messages("log.log")  # this will include the error and fatal messages as well as the debug, info, and warn messages
