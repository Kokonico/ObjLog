# LogNode API reference

## Parameters
Defined when creating a new LogNode.

### `name`

- **Type**: `string`
- **default**: ***REQUIRED***
- **Description**: The name of the log node.
- **Example**: `'my log node'`
- **Note**: There are no restrictions on the name, you can add any spaces, special characters, etc.

### `log_file`

- **Type**: `string`, `None`
- **default**: `None`
- **Description**: The path to the log file
- **Example**: `'my_log_file.log'`
- **Note**: Supports relative and absolute paths. If `None`, no log file will be created.

### `print_to_console`

- **Type**: `bool`
- **default**: `False`
- **Description**: Whether to print the log to the console.
- **Example**: `True`

### `print_filter`

- **Type**: `list[LogMessage]`, `None`
- **default**: `None`
- **Description**: A filter for which types of messages to print to the console.
- **Example**: `[Error, Warn]`
- **Note**: If `None`, all messages will be printed.

### `max_messages_in_memory`

- **Type**: `int`
- **default**: `500`
- **Description**: The maximum number of messages to keep in memory. Used to prevent memory leaks.
- **Example**: `1000`
- **Note**: If the number of messages in memory exceeds this number, the oldest messages will be removed.

### `max_log_messages`

- **Type**: `int`
- **default**: `1000`
- **Description**: The maximum number of messages to keep in the log file. Used to prevent log files from growing too
  large.
- **Example**: `10000`
- **Note**: If the number of messages in the log file exceeds this number, the oldest messages will be removed.

### `log_when_closed`

- **Type**: `bool`
- **default**: `True`
- **Description**: Whether to log a message indicating that the log node was closed.
- **Example**: `False`

### `wipe_log_file_on_init`

- **Type**: `bool`
- **default**: `False`
- **Description**: Whether to wipe the log file when the log node is initialized.
- **Example**: `True`
- **Note**: If `False`, the log file will be appended to, if true, the log file will be overwritten, than appended to.

## Methods

### `log`

- **Description**: Logs a message to the log node.
- **Returns**: `None`

- **Parameters**:

  - #### `message`
    - **Type**: `LogMessage, Exception, BaseException`
    - **Default**: ***REQUIRED***
    - **Description**: The message to log.
    - **Example**: `'Info("Hello, world!")'

  - #### `override_log_file`
    - **Type**: `string`, `None`
    - **Default**: `None`
    - **Description**: The path to the log file to use for this message. If `None`, the log file defined in the log node
      will be used.
    - **Example**: `'my_log_file.log'`
    - **Note**: Supports relative and absolute paths.

  - #### `force_print`
    - **Type**: `tuple(bool, bool)`
    - **Default**: `(False, False)`
    - **Description**: A tuple of two booleans. The first boolean is whether to force print to the console, the second
      boolean is the to print or not.
    - **Example**: `(True, False)` (force don't print to console)

    - #### `preserve_message_in_memory`
    - **Type**: `bool`
    - **Default**: `True`
    - **Description**: Whether to preserve the message in memory. If `False`, the message will not be stored in memory.
    - **Example**: `False`
    - **Note**: Mostly used for internal purposes. If you are not sure, leave it as `True`.

### `set_output_file`

- **Description**: Sets the log file for the entire log node.
- **Returns**: `None`
- **Parameters**:

  - #### `file`
    - **Type**: `string`, `None`
    - **Default**: ***REQUIRED***
    - **Description**: The path to the log file to use for this message. If `None`, the log file is removed.
    - **Example**: `'my_log_file.log'`
    - **Note**: Supports relative and absolute paths.
  - #### `preserve_old_messages`
    - **Type**: `bool`
    - **Default**: `False`
    - **Description**: Whether to bring previously logged messages to the new log file.
    - **Example**: `False`
    - **Note**: If `False`, any messages logged before this method is called will not be in the new log file.

### `dump_messages`
  - **Description**: Dumps all messages in memory to a file.
  - **Returns**: `None`
  - **Parameters**:

    - #### `file`
      - **Type**: `string`
      - **Default**: ***REQUIRED***
      - **Description**: The path to the file to dump the messages to.
      - **Example**: `'my_log_file.log'`
      - **Note**: Supports relative and absolute paths.
    
    - #### `elementfilter`
      - **Type**: `list[LogMessage]`, `None`
      - **Default**: `None`
      - **Description**: A filter for which types of messages to dump to the file.
      - **Example**: `[Error, Warn]`
      - **Note**: If `None`, all messages will be dumped.
    
    - #### `wipe_messages_from_memory`
      - **Type**: `bool`
      - **Default**: `False`
      - **Description**: Whether to remove the messages from memory after dumping them to the file.
      - **Example**: `True`
      - **Note**: If `True`, the messages will be removed from memory after dumping them to the file.
    
### `filter`
  - **Description**: Filters the messages within the log node to specific types.
  - **Returns**: `None`
  - **Parameters**:
    - #### `typefilter`
      - **Type**: `list[LogMessage]`, `None`
      - **Default**: ***REQUIRED***
      - **Description**: A function to filter the messages within the log node, it will keep only the messages that are in the list.
      - **Example**: `[Error, Warn]`
    
    - #### `filter_logfiles`
      - **Type**: `bool`
      - **Default**: `False`
      - **Description**: Whether to filter the log file after filtering the messages in memory.
      - **Example**: `True`

### `dump_messages_to_console`
  - **Description**: Dumps all messages in memory to the console.
  - **Returns**: `None`
  - **Parameters**:
    - #### `elementfilter`
      - **Type**: `list[LogMessage]`, `None`
      - **Default**: `None`
      - **Description**: A filter for which types of messages to dump to the console.
      - **Example**: `[Error, Warn]`
      - **Note**: If `None`, all messages will be dumped.

### `wipe_messages`
  - **Description**: Wipes all messages from memory.
  - **Returns**: `None`
  - **Parameters**:
    - #### `wipe_logfiles`
      - **Type**: `bool`
      - **Default**: `False`
      - **Description**: Whether to wipe the log file as well.
      - **Example**: `True`
      - **Note**: If `True`, the log file will be wiped as well.

### `clear_log`
  - **Description**: Clears the log file.
  - **Returns**: `None`

### `set_max_messages_in_log`
  - **Description**: Sets the maximum number of messages to keep in the log file.
  - **Returns**: `None`
  - **Parameters**:
    - #### `max_file_size`
      - **Type**: `int`
      - **Default**: ***REQUIRED***
      - **Description**: The maximum number of messages to keep in the log file.
      - **Example**: `10000`

### `get`
  - **Description**: Gets the messages in memory.
  - **Returns**: `list[LogMessage]`
  - **Parameters**:
    - #### `elementfilter`
      - **Type**: `list[LogMessage]`, `None`
      - **Default**: `None`
      - **Description**: Retrieve only the messages that passed in.
      - **Example**: `Error, Warn`
      - **Note**: If `None`, all messages will be returned. If more than one argument is passed, if a message matches at least one of the arguments, it will be returned.

### `combine`
  - **Description**: Combines two or more log nodes into one.
  - **Returns**: `None`
  - **Parameters**:
    - #### `other`
      - **Type**: `LogNode`
      - **Default**: ***REQUIRED***
      - **Description**: The log node to merge into the current one.
      - **Example**: `LogNode("my epic log node")`
    - #### `merge_log_files`
      - **Type**: `bool`
      - **Default**: `True`
      - **Description**: Whether to merge the log files of the log nodes.
      - **Example**: `True`
      - **Note**: If `True`, the log files will be merged into one, the other log file will stay.
  - **Note**: The log node that is being combined into the current one will not be affected, however the current log node will get all the messages from the other log node at that time, they will not be linked afterwards.

### `squash`
  - **Description**: Squashes a LogNode into a single message.
  - **Returns**: `None`
  - **Parameters**:
    - #### `message`
      - **Type**: `str`
      - **Default**: ***REQUIRED***
      - **Description**: The message to squash the log node into.
      - **Example**: `This is a squashed message`
  
### dunders

 - #### `__repr__`
    - **Description**: Returns a string representation of the log node.
    - **Returns**: `str`
    - **Example**: `LogNode example at output console`, `LogNode example at output log.log`

 - #### `__len__`
    - **Description**: Returns the number of messages in memory.
    - **Returns**: `int`
    - **Example**: `10`

 - #### `__contains__`
    - **Description**: Checks if the log node has a specific message.
    - **Returns**: `bool`
    - **Parameters**:
      - #### `message`
        - **Type**: `LogMessage`
        - **Default**: ***REQUIRED***
        - **Description**: The message to check for.
        - **Example**: `Error, Warn, Info`
  