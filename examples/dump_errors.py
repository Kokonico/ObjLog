"""dump all warnings, errors, and fatal errors to a file using ObjLog"""

from objlog import LogNode
from objlog.LogMessages import Debug, Info, Warn, Error, Fatal

# create a log node
log = LogNode(name="Error Dump Example")

log.log(Debug("This is a debug message"))
log.log(Info("This is an info message"))
log.log(Warn("This is a warning message"))
log.log(Error("This is an error message"))
log.log(Fatal("This is a fatal error message"))

# dump all messages to a file

log.dump_messages("messages.log")

# dump all messages to the console

log.dump_messages_to_console()

# you can filter the messages by element type for both dump_messages and dump_messages_to_console,
# for example, to dump only warnings and fatal errors to the console:

log.dump_messages_to_console(Warn, Fatal)

# or to dump only debug messages to a file:

log.dump_messages("debug.log", elementfilter=[Debug])
