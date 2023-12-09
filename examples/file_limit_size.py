"""Limit file size example in ObjLog."""

from objlog import LogNode
from objlog.LogMessages import Debug, Info, Warn, Error, Fatal

# Create a log node with a file message limit of 5 messages.

log = LogNode('Log Size Limitation', log_file='log_size_limit.log', max_log_messages=5)

# Log some messages.

log.log(Debug('This is a test message.'))
log.log(Info('This is a test message.'))
log.log(Warn('This is a test message.'))
log.log(Error('This is a test message.'))
log.log(Fatal('This is a test message.'))

# Log some more messages.

log.log(Debug('This is a also a test message.'))

# the log file should now contain only the last 5 messages.

# optionally, you can limit both the file size and the number of messages in memory.

log = LogNode('Log Size Limitation', log_file='log_size_limit.log', max_log_messages=5, max_messages_in_memory=5)
