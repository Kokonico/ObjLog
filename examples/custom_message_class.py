"""custom message classes can be used to add additional information to the log messages in ObjLog"""

from objlog import LogNode, LogMessage
from objlog.LogMessages import Debug, Info, Warn, Error, Fatal

log = LogNode(name="Custom Message Class Example", print_to_console=True)

log.log(Debug("debug message"))
log.log(Info("info message"))
log.log(Warn("warn message"))
log.log(Error("error message"))
log.log(Fatal("fatal message"))

# custom message classes can be used to add additional information to the log messages in ObjLog
# the only requirement is that the message class inherits from LogMessage, and has the following attributes:

# - level: name of the log message

# - color: color of the log message, in standard python color coding, (ex: "\033[93m" for yellow)

class CustomMessage(LogMessage):
    """a custom message class"""
    level = "CUSTOM"
    color = "\033[96m"


log.log(CustomMessage("custom message"))

# the message will be printed in the color specified in the color attribute
# the level attribute is used to determine the level of the message, and is used for filtering

# filtering custom messages works the same as filtering built-in messages
# see examples/filter_messages.py for more information
