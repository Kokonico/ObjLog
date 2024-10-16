"""log python errors with objlog"""

from objlog import LogNode
from objlog.LogMessages import Debug, Info, Warn, Error, Fatal

# create a log node

log = LogNode(name="Error Catching Example", print_to_console=True)

# do some logging

log.log(Debug("this is a debug message"))
log.log(Info("this is an info message"))
log.log(Warn("this is a warning message"))
log.log(Error("this is an error message"))
log.log(Fatal("this is a fatal message"))

# log python exceptions

try:
    1 / 0
except Exception as e:
    log.log(e)

log.log(ImportError("this is an ImportError"))
