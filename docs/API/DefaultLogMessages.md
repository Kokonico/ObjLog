# Default Log Messages

## Importing

```python
from objlog.LogMessages import Info, Debug, Warn, Error, Fatal, PythonExceptionMessage
```

## `Info`

```python
log.log(Info("Hello, world!"))
```

- **Description**: Logs an informational message.
- **color**: Green

## `Debug`

```python
log.log(Debug("Hello, world!"))
```

- **Description**: Logs a debug message.
- **color**: Blue

## `Warn`

```python
log.log(Warn("Hello, world!"))
```

- **Description**: Logs a warning message.
- **color**: Yellow

## `Error`

```python
log.log(Error("Hello, world!"))
```

- **Description**: Logs an error message.
- **color**: Red

## `Fatal`

```python
log.log(Fatal("Hello, world!"))
```

- **Description**: Logs a fatal message.
- **color**: Pink

## `PythonExceptionMessage`

```python
try:
    raise Exception("Hello, world!")
except Exception as e:
    log.log(e)
```

- **Description**: An object wrapping a Python exception, not to be used directly, but to interact with exceptions logged to the LogNode.
- **color**: Red
- **Note**: When getting the exception from the LogNode, it will be wrapped in a `PythonExceptionMessage` object. which is a subclass of `LogMessage`. to get the original exception, you can use the `.exception` attribute of the `PythonExceptionMessage` object.
Any attributes or methods of a LogMessage can be used on a `PythonExceptionMessage` object, and the original exception object can be accessed using the `.exception` attribute.
