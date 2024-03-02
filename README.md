# ObjLog
> logging, Objectified

## Notice

This repo is a living repository, and the master branch is not guaranteed to be stable. If you want to use this library in a project, please use a release version, or a tagged commit.
It is always in the works, and new features are being added all the time!

## what is this?
This is a logging library for python. It is designed to be simple to use, and easy to understand.

## how do I use it?
You can use it like this:

```python
from objlog import LogNode
from objlog.LogMessages import Debug, Info, Warn, Error, Fatal

log = LogNode(name="Basic Example", print_to_console=True)

log.log(Debug("this is a debug message"))
log.log(Info("this is an info message"))
log.log(Warn("this is a warning message"))
log.log(Error("this is an error message"))
log.log(Fatal("this is a fatal message"))
```

output:
```shell
[Basic Example] [2023-12-08 08:36:33.155] DEBUG: This is a debug message
[Basic Example] [2023-12-08 08:36:33.155] INFO: This is an info message
[Basic Example] [2023-12-08 08:36:33.155] WARN: This is a warning message
[Basic Example] [2023-12-08 08:36:33.155] ERROR: This is an error message
[Basic Example] [2023-12-08 08:36:33.155] FATAL: This is a fatal message
```

(it's even colored in the console!)

## This is cool, but I want to do more!

### I want to log to a file!

```python
from objlog import LogNode
from objlog.LogMessages import Debug, Info, Warn, Error, Fatal

log = LogNode(name="File Example", print_to_console=True, log_file="example.log")

log.log(Debug("this is a debug message"))
log.log(Info("this is an info message"))
log.log(Warn("this is a warning message"))
log.log(Error("this is an error message"))
log.log(Fatal("this is a fatal message"))
```

output:
```shell
[File Example] [2023-12-08 08:36:33.155] DEBUG: This is a debug message
[File Example] [2023-12-08 08:36:33.155] INFO: This is an info message
[File Example] [2023-12-08 08:36:33.155] WARN: This is a warning message
[File Example] [2023-12-08 08:36:33.155] ERROR: This is an error message
[File Example] [2023-12-08 08:36:33.155] FATAL: This is a fatal message
```

example.log:
```shell
[File Example] [2023-12-08 08:36:33.155] DEBUG: This is a debug message
[File Example] [2023-12-08 08:36:33.155] INFO: This is an info message
[File Example] [2023-12-08 08:36:33.155] WARN: This is a warning message
[File Example] [2023-12-08 08:36:33.155] ERROR: This is an error message
[File Example] [2023-12-08 08:36:33.155] FATAL: This is a fatal message
```

### I want a custom log message type!

```python
from objlog import LogNode, LogMessage
from objlog.LogMessages import Debug, Info, Warn, Error, Fatal

class CustomMessage(LogMessage):
    color = "\033[32" # green
    level = "CUSTOM"

log = LogNode(name="Custom Example", print_to_console=True)

log.log(CustomMessage("this is a custom message"))
```

output:
```shell
[Custom Example] [2023-12-08 08:36:33.155] CUSTOM: This is a custom message
```

(colored green in the console!)


### I want to log messages, but not print them to the console or a log file, than when I'm done, I want to print them all at once!

```python
from objlog import LogNode, LogMessage
from objlog.LogMessages import Debug, Info, Warn, Error, Fatal

log = LogNode(name="Buffered Example")

log.log(Debug("this is a debug message"))
log.log(Info("this is an info message"))
log.log(Warn("this is a warning message"))
log.log(Error("this is an error message"))
log.log(Fatal("this is a fatal message"))

log.dump_messages("example.log")  # this will not print the messages to the console, but save them to a file
# or
log.dump_messages_to_console()  # this will print the messages to the console, but not save them to a file

# you can do both if you want!

# if you would like to continue logging after dumping the messages, you can do that too!
```

output:
```shell
[Buffered Example] [2023-12-08 08:36:33.155] DEBUG: This is a debug message
[Buffered Example] [2023-12-08 08:36:33.155] INFO: This is an info message
[Buffered Example] [2023-12-08 08:36:33.155] WARN: This is a warning message
[Buffered Example] [2023-12-08 08:36:33.155] ERROR: This is an error message
[Buffered Example] [2023-12-08 08:36:33.155] FATAL: This is a fatal message
```

example.log:
```shell
[Buffered Example] [2023-12-08 08:36:33.155] DEBUG: This is a debug message
[Buffered Example] [2023-12-08 08:36:33.155] INFO: This is an info message
[Buffered Example] [2023-12-08 08:36:33.155] WARN: This is a warning message
[Buffered Example] [2023-12-08 08:36:33.155] ERROR: This is an error message
[Buffered Example] [2023-12-08 08:36:33.155] FATAL: This is a fatal message
```

### Amazing! How do I filter messages?

```python
from objlog import LogNode, LogMessage
from objlog.LogMessages import Debug, Info, Warn, Error, Fatal

log = LogNode(name="Filter Example")

log.log(Debug("this is a debug message"))
log.log(Info("this is an info message"))
log.log(Warn("this is a warning message"))
log.log(Error("this is an error message"))
log.log(Fatal("this is a fatal message"))

log.dump_messages("example.log", elementfilter=[Warn, Error, Fatal])  # this will not print the messages to the console, but save them to a file if they are a warning, error, or fatal
# the rest of the messages will not be saved to the file

# you can do the same thing with dump_messages_to_console()

log.dump_messages_to_console(elementfilter=[Warn, Error, Fatal])

# you can also filter the log in-place

log.filter(typefilter=[Warn, Error, Fatal])  # this will remove all messages that are not a warning, error, or fatal from the log's memory

# you can also use the filter method to filter the logfile

log.filter(typefilter=[Warn, Error, Fatal], filter_logfiles=True)  # this will remove all messages that are not a warning, error, or fatal from the log's memory, and overwrite the logfile with the filtered messages

# it even works with custom message types!

class CustomMessage(LogMessage):
    color = "\033[32" # green
    level = "CUSTOM"

log.log(CustomMessage("this is a custom message"))
log.log(CustomMessage("this is another custom message"))
log.log(Info("this is an info message"))

log.dump_messages_to_console(elementfilter=[CustomMessage])  # this will only print the custom messages to the console

# output:
# [Filter Example] [2023-12-08 08:36:33.155] CUSTOM: This is a custom message
# [Filter Example] [2023-12-08 08:36:33.155] CUSTOM: This is another custom message
```

### I want to not have a log file, and then I want to switch to having a log file (and store my old messages in it)!

```python
from objlog import LogNode, LogMessage
from objlog.LogMessages import Debug, Info, Warn, Error, Fatal

log = LogNode(name="Switch Example")  # no log file

log.log(Debug("this is a debug message"))
log.log(Info("this is an info message"))
log.log(Warn("this is a warning message"))
log.log(Error("this is an error message"))
log.log(Fatal("this is a fatal message"))

log.set_output_file("example.log")  # now there is a log file, all new messages will be saved to it

log.log(Debug("this is a debug message 2")) # this message will be saved to the log file
log.log(Info("this is an info message 2"))  # this message will be saved to the log file
log.log(Warn("this is a warning message 2"))  # this message will be saved to the log file
log.log(Error("this is an error message 2"))  # this message will be saved to the log file
log.log(Fatal("this is a fatal message 2"))  # this message will be saved to the log file

# the messages before the log file was set will not be saved to the log file

# to move the old messages to the log file, you can do this:

log.set_output_file("example2.log", preserve_old_messages=True)  # now the old messages will be saved to the log file, and all new messages will be saved to it as well

log.log(Debug("this is a debug message 3")) # this message will be saved to the log file
```

example.log:
```shell
[Switch Example] [2023-12-08 08:36:33.155] DEBUG: This is a debug message 2
[Switch Example] [2023-12-08 08:36:33.155] INFO: This is an info message 2
[Switch Example] [2023-12-08 08:36:33.155] WARN: This is a warning message 2
[Switch Example] [2023-12-08 08:36:33.155] ERROR: This is an error message 2
[Switch Example] [2023-12-08 08:36:33.155] FATAL: This is a fatal message 2
```

example2.log:
```shell
[Switch Example] [2023-12-08 08:36:33.155] DEBUG: This is a debug message
[Switch Example] [2023-12-08 08:36:33.155] INFO: This is an info message
[Switch Example] [2023-12-08 08:36:33.155] WARN: This is a warning message
[Switch Example] [2023-12-08 08:36:33.155] ERROR: This is an error message
[Switch Example] [2023-12-08 08:36:33.155] FATAL: This is a fatal message
[Switch Example] [2023-12-08 08:36:33.155] DEBUG: This is a debug message 2
[Switch Example] [2023-12-08 08:36:33.155] INFO: This is an info message 2
[Switch Example] [2023-12-08 08:36:33.155] WARN: This is a warning message 2
[Switch Example] [2023-12-08 08:36:33.155] ERROR: This is an error message 2
[Switch Example] [2023-12-08 08:36:33.155] FATAL: This is a fatal message 2
[Switch Example] [2023-12-08 08:36:33.155] DEBUG: This is a debug message 3
```

### I have a very limited amount of RAM, and I want to limit the amount of messages that are stored in memory!

```python
from objlog import LogNode
from objlog.LogMessages import Debug, Info, Warn, Error, Fatal

log = LogNode(name="Limited Example", max_messages_in_memory=5, log_file="limited.log")  # only store 5 messages in memory

log.log(Debug("this is a debug message 1"))
log.log(Info("this is an info message 1"))
log.log(Warn("this is a warning message 1"))
log.log(Error("this is an error message 1"))
log.log(Fatal("this is a fatal message 1"))

log.log(Debug("this is a debug message 2"))  # this message will be stored in memory, and the oldest message will be removed from memory
```

limited.log:
```shell
[Limited Example] [2023-12-08 08:36:33.155] INFO: This is an info message 1
[Limited Example] [2023-12-08 08:36:33.155] WARN: This is a warning message 1
[Limited Example] [2023-12-08 08:36:33.155] ERROR: This is an error message 1
[Limited Example] [2023-12-08 08:36:33.155] FATAL: This is a fatal message 1
[Limited Example] [2023-12-08 08:36:33.155] DEBUG: This is a debug message 2
```

### I have a limited amount of SSD space, and I want to limit the amount of messages that are stored in the log file!

```python
from objlog import LogNode
from objlog.LogMessages import Debug, Info, Warn, Error, Fatal

log = LogNode(name="Limited Example", max_log_messages=5, log_file="limited.log")  # only store 5 messages in the log file, but unlimited messages in memory

log.log(Debug("this is a debug message 1"))
log.log(Info("this is an info message 1"))
log.log(Warn("this is a warning message 1"))
log.log(Error("this is an error message 1"))
log.log(Fatal("this is a fatal message 1"))

log.log(Debug("this is a debug message 2"))  # this message will be stored in the log, and the oldest message will be removed from the log

log.dump_messages_to_console()  # this will print all messages in memory to the console (including ones not saved to the log), but not save them to the log file

# to limit both the amount of messages in memory and the amount of messages in the log file, you can do this:

log = LogNode(name="Limited Example", max_messages_in_memory=5, max_log_messages=5, log_file="limited.log")  # only store 5 messages in the log file, and only store 5 messages in memory
```

output:
```shell
[Limited Example] [2023-12-08 08:36:33.155] DEBUG: This is a debug message 1
[Limited Example] [2023-12-08 08:36:33.155] INFO: This is an info message 1
[Limited Example] [2023-12-08 08:36:33.155] WARN: This is a warning message 1
[Limited Example] [2023-12-08 08:36:33.155] ERROR: This is an error message 1
[Limited Example] [2023-12-08 08:36:33.155] FATAL: This is a fatal message 1
[Limited Example] [2023-12-08 08:36:33.155] DEBUG: This is a debug message 2
```

limited.log:
```shell
[Limited Example] [2023-12-08 08:36:33.155] INFO: This is an info message 1
[Limited Example] [2023-12-08 08:36:33.155] WARN: This is a warning message 1
[Limited Example] [2023-12-08 08:36:33.155] ERROR: This is an error message 1
[Limited Example] [2023-12-08 08:36:33.155] FATAL: This is a fatal message 1
[Limited Example] [2023-12-08 08:36:33.155] DEBUG: This is a debug message 2
```

### I want to log messages, but I don't want to print them to the console or a log file, and I don't want to store them in memory!

1, that's useless why? and 2, you can do that!

```python
from objlog import LogNode
from objlog.LogMessages import Debug, Info, Warn, Error, Fatal

log = LogNode(name="Buffered Example", max_messages_in_memory=0)

log.log(Debug("this is a debug message"))
log.log(Info("this is an info message"))
log.log(Warn("this is a warning message"))
log.log(Error("this is an error message"))
log.log(Fatal("this is a fatal message"))
```

output:
```shell
```

## I want more examples!

check out the [example's](examples) folder within this project, plenty of examples there!

## I want to use this in a project!
Feel free to! This project is licensed under the Zlib license, so you can use it in any project, commercial or not, as long as you give credit to the original author (me) and don't claim it as your own.

## I want to contribute!
Feel free to!
Fork the repo, make your changes, and submit a pull request!
I'll review it, and if it's good, I'll merge it!

(for more information, see [CONTRIBUTING](CONTRIBUTING.md))

## I want to report a bug or request a feature!
Feel free to! Just open an issue, and I'll look into it!

## I found a security vulnerability!
Please don't open an issue for that! Instead, either make a pull request with the fix, or submit a vulnerability report! please read [SECURITY](SECURITY.md) for more information.
