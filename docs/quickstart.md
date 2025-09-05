# Quick Start
## Introduction

This is a quick start guide to get you up and running with ObjLog. This guide will cover the basics of setting up a
LogNode, logging messages, and configuring the logger.

## Installation

ObjLog can be installed via pip:
```bash

pip install objlog
```
or via poetry:

```bash
poetry add objlog
```

## Setting up a LogNode

The first step to using ObjLog is to create a LogNode.
A LogNode is a single logger that can be used to log messages.

To create a LogNode, you can use the `LogNode` class:

```python
from objlog import LogNode

log = LogNode("my logger")
```

(ps: the name of the logger is required, but there are no hard and fast rules about what it should be, so you can name it whatever you want)

## Logging Messages

Once you have a LogNode, you can use it to log messages.

however, you cannot just use the `log` parameter on its own, you need to pass a `LogMessage` to it.

### LogMessages

A `LogMessage` is a message that can be logged. It contains the message, the level of the message, and the time the message was logged.

LogMessages shouldn't be created directly via the `LogMessage` class, but instead via a subclass of it.

ObjLog comes with a few built-in subclasses of `LogMessage`:

- `Debug`
- `Info`
- `Warn`
- `Error`
- `Fatal`

(Note): to learn more about the built-in LogMessages, you can check the [Default LogMessages page](API/DefaultLogMessages.md)

You can use these to log messages to the LogNode:

```python
from objlog import LogNode
from objlog.LogMessages import Info

log = LogNode("my logger")

log.log(Info("Hello, world!"))
```
However, you may notice that no messages are being printed to the console, or to a file, or anywhere else. This is because the LogNode is not configured to output messages anywhere.

## Configuring the LogNode

To configure the LogNode, you must modify the parameters of the LogNode when you create it.

The `LogNode` class has many parameters that can be modified, but we will only cover the most important ones here.

- `name`: The name of the logger. This is required.
- `log_file`: The file to log messages to. If this is not set, messages will not be logged to a file.
- `print_to_console`: Whether to print messages to the console. If this is not set, messages will not be printed to the
  console.
- `print_filter`: the types of messages to print to the console. If this is not set, all messages will be printed to the
  console, regardless of type.

Now we can make the LogNode print messages to the console:

```python
from objlog import LogNode
from objlog.LogMessages import Info

log = LogNode("my logger", print_to_console=True)

log.log(Info("Hello, world!"))
```

Now, when you run the script, you should see something like this (your date and time will be different):

```bash
[my logger] [2024-02-24 12:55:13.609] INFO: Hello, World!
```

notice that the message is prefixed with the name of the logger, this means that you can have multiple loggers in your program, and you can tell which logger is logging the message.

```python
from objlog import LogNode
from objlog.LogMessages import Info

log1 = LogNode("logger 1", print_to_console=True)
log2 = LogNode("logger 2", print_to_console=True)

log1.log(Info("Hello, world!"))
log2.log(Info("Hello, world!"))
```

This will output:

```bash
[logger 1] [2024-02-24 12:55:13.650] INFO: Hello, World!
[logger 2] [2024-02-24 12:55:13.650] INFO: Hello, World!
```

now your logger will print messages to the console, but what if you want to only print messages of a certain type, like only errors?

You can do this by setting the `print_filter` parameter:

```python
from objlog import LogNode
from objlog.LogMessages import Info, Error

log = LogNode("my logger", print_to_console=True, print_filter=[Error])

log.log(Info("Hello, world!"))
log.log(Error("Hello, world!"))
```

This will output:

```bash
[my logger] [2024-02-24 12:55:13.650] ERROR: Hello, World!
```

Now, only messages of type `Error` will be printed to the console.

now, what if you want to log messages to a file?

You can do this by setting the `log_file` parameter:

```python
from objlog import LogNode
from objlog.LogMessages import Info, Error

log = LogNode("my logger", print_to_console=True, log_file="log.log")

log.log(Info("Hello, world!"))
log.log(Error("Hello, world!"))
```

This will output:

```bash
[my logger] [2024-02-24 12:55:13.650] INFO: Hello, World!
[my logger] [2024-02-24 12:55:13.650] ERROR: Hello, World!
```

And the file `log.log` will contain:

```bash
[my logger] [2024-02-24 12:55:13.650] INFO: Hello, World!
[my logger] [2024-02-24 12:55:13.650] ERROR: Hello, World!
```

Now you have a basic understanding of how to use ObjLog, and you can start logging messages in your programs.

For more complex uses, please refer to the [advanced guide](advanced.md).
