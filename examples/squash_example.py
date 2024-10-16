"""squash example for objlog"""

from objlog import LogNode
from objlog.LogMessages import Debug, Info

# create a LogNode
node = LogNode("squash_example", "squash_example.log")

# log thousands of messages

for i in range(1000):
    node.log(Info(f"message {i}"))

node.dump_messages_to_console()  # dump all messages to the console (will take a while)

# squash the log file
node.squash(Debug("squashed log file"))  # now instead of 1000 messages, there's only 1 (the squash message)

print("=" * 100)

node.dump_messages_to_console()  # will only dump 1 message
