"""Filter messages from a log in ObjLog"""

from objlog import LogNode, LogMessage
from objlog.LogMessages import Debug, Info, Warn, Error, Fatal

log = LogNode(name="Filter Messages Example", print_to_console=True, log_file="filter_messages.log")

log.log(Debug("debug message"))
log.log(Info("info message"))
log.log(Warn("warn message"))
log.log(Error("error message"))
log.log(Fatal("fatal message"))

# filtering messages is easy in ObjLog

# to filter the messages in memory, use the filter() method

# the filter() method takes a list of message classes to keep, and removes all other messages from memory

# for example, to filter out all messages except for Debug messages, use the following code:

log.filter([Debug])

# now, only Debug messages are in memory, but the log file still contains all messages
# and new non-Debug messages will still be stored in memory

# to filter the messages in the log file, set the filter_logfiles parameter to True

log.filter([Debug], filter_logfiles=True)

# now, the log file only contains Debug messages.

# as of now, there is no way to filter messages from the log file without filtering them from memory too
# there is also no way to prevent new non-whitelisted messages from being stored in memory
