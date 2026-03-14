# LogMessage API Reference

## Parameters

### `message`

- **Type**: `string`
- **Default**: ***REQUIRED***
- **Description**: The message to log.
- **Example**: `Hello, World!`

## Attributes

### `time_ns`
- **Type**: `integer`
- **Description**: The time the LogMessage was created in nanoseconds.
- **Example**: `1617225013000000000`

### `unix`
- **Type**: `integer`
- **Description**: The unix timestamp that the LogMessage was created, in milliseconds.
- **Example**: `1617225013000`

### `uuid`
- <span style="color:orange">**Deprecated!**</span> Will be removed in 4.0.0, if you need a unique identifier for the LogNode, use python's built-in `id()` function or assign your own unique identifier to the LogNode using a custom attribute.
- **Type**: `string`
- **Description**: The unique identifier for the LogMessage.
- **Example**: `1729141302148986000-187`

### `message`
- **Type**: `string`
- **Description**: The message that was logged, in plain text.
- **Example**: `Hello, World!`

### `level`
- **Type**: `string`
- **Description**: The level of the log message.
- **Example**: `INFO`, `ERROR`, `WARN`, `DEBUG`

### `color`
- **Type**: `string`
- **Description**: The ANSI color code for the level of the log message.
- **Example**: `\033[1;32m`

### `exception`
- **Type**: `Exception`, `None`
- **Description**: The original Python exception object. Only present (non-`None`) if the LogMessage is a `PythonExceptionMessage`. For all other LogMessage subclasses, this is `None`.

## Methods

### `colored`
- **Description**: Returns the message as a string with ANSI color codes.
- **Returns**: `string`

### Dunders

- #### `__str__`
  - **Description**: Returns the message as a string (without ANSI color coding)
  - **Returns**: `string`

- #### `__repr__`
    - **Description**: Nearly identical to `__str__` but does not include the timestamp.
    - **Returns**: `string`

- #### `__eq__`
    - **Description**: Compares the `uuid` of two LogMessages, if they are the same, returns `True`, otherwise `False`.
    - **Returns**: `bool`

- #### `__ne__`
    - **Description**: Compares the `uuid` of two LogMessages, if they are different, returns `True`, otherwise `False`.
    - **Returns**: `bool`