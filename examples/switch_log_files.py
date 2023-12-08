"""swap log files in ObjLog"""

from objlog import LogNode
from objlog.LogMessages import Debug, Info, Warn, Error, Fatal

log = LogNode(name="Switch Log Files Example", print_to_console=True)

log.log(Debug("debug message"))
log.log(Info("info message"))
log.log(Warn("warn message"))
log.log(Error("error message"))
log.log(Fatal("fatal message"))

# you can swap log files in ObjLog by using the set_output_file method

log.set_output_file("log1.log")

log.log(Debug("debug message 1"))

# the contents of the log file will just contain debug message 1

# to preserve the old messages, you can use the preserve_old_messages argument

log.set_output_file("log2.log", preserve_old_messages=True)

# now the contents of log2.log will contain all the messages, even the ones sent before the log file was changed.
