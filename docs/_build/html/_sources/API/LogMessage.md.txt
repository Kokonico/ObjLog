# LogMessage API Reference

## Parameters

### `message`

- **Type**: `string`
- **Default**: ***REQUIRED***
- **Description**: The message to log.
- **Example**: `Hello, World!`

## Variables

### `unix_timestamp`
- **Type**: `integer
- **Default**: ***SET AUTOMATICALLY***
- **Description**: The unix timestamp that the LogMessage was created.
- **Example**: `1617225013`
- ***WARNING***: this is a deprecated variable and will be removed in a future release (2.0.0), please use `unix` instead.

### `unix`
- **Type**: `integer
- **Default**: ***SET AUTOMATICALLY***
- **Description**: The unix timestamp that the LogMessage was created.
- **Example**: `1617225013`
- **Note**: this is identical to `unix_timestamp` and is the recommended variable to use.

### `uuid`
- **Type**: `string`
- **Default**: ***SET AUTOMATICALLY***
- **Description**: The unique identifier for the LogMessage.
- **Example**: `1617225013-123`

## Methods

### `colored`
- **Description**: Returns the message as a string with ANSI color codes.
- **Returns**: `string`

### Dunders

- #### `__str__`
  - **Description**: Returns the message as a string (without ANSI color coding)
  - **Returns**: `string`

- #### `__repr__`
    - **Description**: Nearly indentical to `__str__` but does not include the timestamp.
    - **Returns**: `string`

- #### `__eq__`
    - **Description**: Compares the `uuid` of two LogMessages, if they are the same, returns `True`, otherwise `False`.
    - **Returns**: `bool`

- #### `__ne__`
    - **Description**: Compares the `uuid` of two LogMessages, if they are different, returns `True`, otherwise `False`.
    - **Returns**: `bool`