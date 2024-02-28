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

*Note: if you are using below 1.2.2, you will need to put `None` in the `get` method, as the `get` method did not automatically select all before then.*

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

prints(log.get()) # prints: []
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

### checking for types of messages

You can check if a certain type of message has been logged to the LogNode by using the `has` method.

```python
log.log(Info("Hello, world!"))

print(log.has(Info)) # prints: True

print(log.has(Debug)) # prints: False
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

## Conclusion

That's it for the advanced guide. You should now have a good understanding of how to use ObjLog in more advanced ways.

for the complete API reference, see the [API reference](api.md).
```
