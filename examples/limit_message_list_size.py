"""example for limiting the size of the logger's message list to prevent memory leaks in ObjLog"""

from objlog import LogNode
from objlog.LogMessages import Debug, Info

# create a logger
logger = LogNode(name="example", max_messages_in_memory=5)

# log some messages

logger.log(Debug("debug message 1"))
logger.log(Debug("debug message 2"))
logger.log(Debug("debug message 3"))
logger.log(Debug("debug message 4"))
logger.log(Debug("debug message 5"))

logger.log(Info("info message 1"))

# the logger will now drop the oldest message (debug message 1) to make room for the new message

logger.dump_messages_to_console()

# change the limit

logger.set_max_messages_in_memory(3)  # this will drop debug message 2 and 3, but keep 4 and 5

# this can be used to prevent memory leaks in long-running applications, as the logger without a limit will grow
# larger and larger.

# By default, the limit is set to 1000 messages. Setting it to None will disable the limit.
# Be careful with this, as it can lead to memory leaks if the logger is used in a long-running application.
