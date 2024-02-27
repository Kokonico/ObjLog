# Advanced guide.

In this guide, we will cover more advanced uses of ObjLog, such as custom LogMessage types,
Logging Python Exceptions, and catching logged errors.

## Custom LogMessage types.

You can create custom LogMessage types by subclassing the `LogMessage` class.

they have two attributes that must be defined for them to work properly:

- `level`: The level of the message. This is a string, and can be any value you want.
- `color`: The color of the message. This is prefixed before the message, and is supposed to be an ansi color code.

Here is an example of a custom LogMessage type:

```python
from objlog import LogMessage

class CustomLogMessage(LogMessage):
    level = "custom"
    color = "\033[35m"
```

it's exactly the same as the built-in LogMessage types, but with a different level and color.

```python
# extends the code from above.

from objlog import LogNode

log = LogNode("my logger")

log.log(CustomLogMessage("Hello, world!"))
```

## Interacting with the LogNode

You can interact with the LogNode in a few ways.

### Getting logged messages

You can get the messages that have been logged to the LogNode by using the `get` method.

```python
from objlog import LogNode
from objlog.LogMessages import Info

log = LogNode("my logger")

log.log(Info("Hello, world!"))

print(log.get()) # prints: [Info("Hello, world!")]
```

you can also filter what types of messages you want to get by passing the specified types to the `get` method.

```python
log.log(Info("Hello, world!"))
log.log(Debug("Hello, world!"))
log.log(Warn("Hello, world!"))

print(log.get(Info, Debug)) # prints: [Info("Hello, world!"), Debug("Hello, world!")]
```

### Clearing logged messages

You can clear the messages that have been logged to the LogNode by using the `wipe_messages` method.

```python
log.log(Info("Hello, world!"))

prints(log.get()) # prints: [Info("Hello, world!")]

log.wipe_messages()

lprints(og.get()) # prints: []
```

keep in mind this will not clear any log files that are being logged to, to do that you can either set the parameter `wipe_logfiles` to True when calling the `wipe_messages` method, or you can call the `clear_log` method if you do not want to wipe the memory.

```python
log.log(Info("Hello, world!"))

prints(log.get()) # prints: [Info("Hello, world!")]

log.wipe_messages(wipe_logfiles=True)

prints(log.get()0 # prints: []

# or

log.log(Info("Hello, world!"))

prints(log.get()) # prints: [Info("Hello, world!")]

log.clear_log()

prints(log.get()) # prints: [Info("Hello, world!")] as it did not wipe memory.
```

it also works with retrieving python exceptions of certain types (more on that later).

```python
log.log(ImportError("Hello, world!"))

print(log.get(ImportError)) # prints: [PythonExceptionMessage("Hello, world!")]
```

### checking for types of messages

You can check if a certain type of message has been logged to the LogNode by using the `has` method.

```python
log.log(Info("Hello, world!"))

print(log.has(Info)) # prints: True

print(log.has(Debug)) # prints: False
```

if you want to find if you have a specific kind of python exception, you can just pass the exception type to the `has`
method.

```python
log.log(ImportError("Hello, world!"))

print(log.has(ImportError)) # prints: True

print(log.has(ValueError)) # prints: False
```

it even works with both combined.

```python
log.log(Info("Hello, world!"))
log.log(ImportError("Hello, world!"))

print(log.has(Info, ImportError)) # prints: True
```

### filtering messages (in place)

You can filter the messages that have been logged to the LogNode by using the `filter` method.

```python
log.log(Info("Hello, world!"))
log.log(Debug("Hello, world!"))
log.log(Warn("Hello, world!"))

log.filter([Info, Debug])

print(log.get()) # prints: [Info("Hello, world!"), Debug("Hello, world!")]
```

optionally, you can filter logfiles as well by setting the `filter_logfiles` parameter to True.

```python
log.log(Info("Hello, world!"))
log.log(Debug("Hello, world!"))
log.log(Warn("Hello, world!"))

log.filter([Info, Debug], filter_logfiles=True)

print(log.get()) # prints: [Info("Hello, world!"), Debug("Hello, world!")]
```
## Logging Python Exceptions

You can log Python exceptions by using the `log` method with an exception instead of a LogMessage.

however, when getting the exception from the LogNode, it will be wrapped in a `PythonExceptionMessage` object. which is a subclass of `LogMessage`.

to get the original exception, you can use the `.exception` attribute of the `PythonExceptionMessage` object.

```python
log.log(ImportError("Hello, world!"))

log.get() # returns: [PythonExceptionMessage("Hello, world!")]

log.get()[0].exception # returns: ImportError("Hello, world!")
```

## Catching Real python exceptions

logging python exceptions is great, but what if you want to catch them when they happen?

you can do it in two ways, try/except, or by using the `@monitor` decorator.

```python
from objlog import LogNode,
from objlog.utils import monitor

log = LogNode("my logger")

try:
    1 / 0
except ImportError as e:
    log.log(e) # logs the exception

@monitor(log)
def my_function():
    1 / 0

my_function() # logs the exception to LogNode 'log' when it occurs
```

## `@monitor` decorator

The `@monitor` decorator is a decorator that logs any exceptions that occur in the function it is decorating.

it has a few parameters:

- `log`: The LogNode to log the exceptions to. This is required.
- `raise_exceptions`: Whether to raise the exception after logging it. This is optional, and defaults to False.
- `exit_on_exception`: Whether to exit the program after logging the exception. This is optional, and defaults to False. It also completely ignores the `raise_exceptions` parameter, regardless of its value.

### `exit_on_exception`

exit on exception is useful for when you want to log an exception and then exit the program in user-facing code.

however, it is not recommended to use it in library code, as it makes debugging harder.

```python

@monitor(log, exit_on_exception=True)
def my_function():
    1 / 0

my_function() # logs the exception to LogNode 'log' when it occurs, and then exits the program.
```

exit on exception acts differently depending on where the lognode outputs to.

if the lognode outputs to a file and doesn't print, it will log the exception and location to where the exception
occurred,
and then exit the program printing a message along the lines of
"An exception occurred: (exception message) please check the log file for more information."

however, if the lognode outputs to the console, it will not print any extra info, and you will see the exception message printed to the console (assuming it's in the print list).

if the LogNode does not output to a file, it will print the whole traceback to the console.

### `raise_exceptions`

raise exceptions is useful for when you want to log an exception and then raise it.

```python

@monitor(log, raise_exceptions=True)
def my_function():
    1 / 0

my_function() # logs the exception to LogNode 'log' when it occurs, and then raises a ZeroDivisionError.
```

raise exceptions does not act differently depending on where the lognode outputs to.

it will always raise the exception after logging it.

it won't do anything extra, it will just raise the exception.

## Conclusion

That's it for the advanced guide. You should now have a good understanding of how to use ObjLog in more advanced ways.

for the complete API reference, see the [API reference](api.md).
```
