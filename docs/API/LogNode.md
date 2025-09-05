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
- **Note**: Can be changed at any time by setting the `print` attribute of the LogNode to `True` or `False`.

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

### `enabled`

- **Type**: `bool`
- **default**: `True`
- **Description**: Whether the log node is enabled. If `False`, `log()` will do nothing and return `None` immediately.
- **Example**: `True`
- **Note**: Can be changed at any time by setting the `enabled` attribute of the LogNode to `True` or `False`, or by using the `enable()` and `disable()` methods.

## Attributes

### `print`
- **Type**: `bool`
- **Description**: Whether the LogNode prints logged messages to the console.
- **Example**: `True`
- **Note**: Can be changed at any time without consequences.

### `name`
- **Type**: `string`
- **Description**: The name of the LogNode.
- **Example**: `'my log node'`
- **Note**: Not recommended to change after initialization, consider using the `rename` method instead.

### `log_file`
- **Type**: `string`, `None`
- **Description**: The path to the log file, if any.
- **Example**: `'my_log_file.log'`
- **Note**: Not recommended to change after initialization, consider using the `set_output_file` method instead.

### `messages`
- **Type**: `deque[LogMessage]`
- **Description**: The messages in memory.
- **Example**: `[Info("Hello, world!"), Error("I am an error!")]`
- **Note**: Extremely not recommended to change manually, modify only using the methods provided.

### `uuid`
- **Type**: `string`
- **Description**: The unique identifier of the LogNode.
- **Example**: `'1729141009132775000-82'`
- **Note**: Heavily advised not to change manually, doing so can cause serious issues.

### `log_when_closed`
- **Type**: `bool`
- **Description**: Returns if the log node logs a message when closed or not.
- **Example**: `True`
- **Note**: Can be changed at any time without consequences.

### `max`
- **Type**: `int`
- **Description**: The maximum number of messages to keep in memory.
- **Example**: `1000`
- **Note**: Should not be changed manually, use the `set_max_messages_in_memory` method instead.

### `maxinf`
- **Type**: `int`
- **Description**: The maximum number of messages to keep in the log file.
- **Example**: `10000`
- **Note**: Should not be changed manually, use the `set_max_messages_in_log` method instead.

## Methods

### `log`

- **Description**: Logs a message to the log node.
- **Returns**: `None`, `dict`

- **Parameters**:

  - #### `messages`
    - **Type**: `LogMessage(s), Exception(s), BaseException(s)`
    - **Default**: ***REQUIRED***
    - **Description**: The message(s) to log.
    - **Example**: `'Info("Hello, world!")'`, `'Info("I am message 1"), Error("I am message 2")'`

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

    - #### `verbose`
    - **Type**: `bool`
    - **Default**: `False`
    - **Description**: Whether to return a list of extra data when the function completes
    - **Example**: `True`
    - **Note**: the return structure is as follows:
    ```python
    {'processtime_ns': 4000, 'logged': [{'message': 'benchmark test', 'id_in_node': 1, 'type': 'INFO'}]}
    ```
    `processtime_ns` is how many nanoseconds it took to log the message, and logged is a list of the messages you logged, as well as their respective indexes
  - `message` is the raw text inputted into the message
  - `id_in_node` is the index of the message in the log node's `messages` deque.
  - `type` is the type of the message as a string, for example, `Info`, `Error`, `Warn`, etc.

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
      - **Type**: `LogMessage(s)/Exception(s)/BaseException(s)`, `None`
      - **Default**: `None`
      - **Description**: A filter for which types of messages to dump to the file.
      - **Example**: `Error, Warn`
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
      - **Type**: `LogMessage(s)/Exception(s)/BaseException(s)`, `None`
      - **Default**: ***REQUIRED***
      - **Description**: A function to filter the messages within the log node, it will keep only the messages that are in the list.
      - **Example**: `Error, Warn, ImportError`
    
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
      - **Type**: `LogMessage(s)/Exception(s)/BaseException(s)`, `None`
      - **Default**: `None`
      - **Description**: A filter for which types of messages to dump to the console.
      - **Example**: `Error, Warn, ImportError`
      - **Note**: If the only element received is `None`, all messages will be dumped.

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

### `set_max_messages_in_memory`:
- **Description**: Sets the maximum number of messages to keep in memory.
- **Returns**: `None`
- **Parameters**:
  - #### `max_messages`
    - **Type**: `int`
    - **Default**: ***REQUIRED***
    - **Description**: The maximum number of messages to keep in memory.
    - **Example**: `1000`

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
    - #### `*elementfilter`
      - **Type**: `Union[LogMessage, Exception, BaseException]`, `None`
      - **Default**: `None`
      - **Description**: Retrieve only the messages that passed in.
      - **Example**: `Error, Warn, ImportError`
      - **Note**: If `None`, all messages will be returned. If more than one argument is passed, if a message matches at least one of the arguments, it will be returned. Also, if you use get() to get a python exception, you will receive a PythonExceptionMessage object, to access the exception, use the `exception` attribute like this: `get(ImportError)[0].exception`.

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
  - **Note**: The log node that is being combined into the current one will not be affected, however, the current log node will get all the messages from the other log node at that time, they will not be linked afterward.

### `squash`
  - **Description**: Squashes a LogNode into a single message.
  - **Returns**: `None`
  - **Parameters**:
    - #### `message`
      - **Type**: `str`
      - **Default**: ***REQUIRED***
      - **Description**: The message to squash the log node into.
      - **Example**: `This is a squashed message`
    - #### `squash_logfile`
      - **Type**: `bool`
      - **Default**: `True`
      - **Description**: Whether to wipe the log file after squashing the log node.
      - **Example**: `False`
      - **Note**: If `True`, the log file will be wiped after squashing the log node and the squashed message will be the only message in the log file.

### `has`
  - **Description**: Checks if the log node has a specific type of message.
  - **Returns**: `bool`
  - **Parameters**:
    - #### `*message`
        - **Type**: `Union[LogMessage, Exception, BaseException]`
        - **Default**: ***REQUIRED***
        - **Description**: The message(s) to check for.
        - **Example**: `Error, Warn, ImportError`
        - **Note**: If more than one argument is passed, if a message matches at least one of the arguments, it will return `True`.
### `has_errors`
  - **Description**: Checks if the log node has any errors.
  - **Returns**: `bool`
  - **Parameters**: `None`
  - **Note**: This is shorthand for `has(Error, Fatal, PythonExceptionMessage)`.


### `rename`
  - **Description**: Renames the log node.
  - **Returns**: `None`
  - **Parameters**:
    - #### `new_name`
      - **Type**: `str`
      - **Default**: ***REQUIRED***
      - **Description**: The new name of the log node.
      - **Example**: `my new log node`
    - #### `update_in_logs`
      - **Type**: `bool`
      - **Default**: `False`
      - **Description**: Whether to update the name of the lognode in the log files.
      - **Example**: `True`
  - **Note**: The name of the log node can be changed at any time, but old messages in the log file will still have the old name next to them unless `update_in_logs` is set to `True`.

### `save`
  - **Description**: Saves the log node to a file.
  - **Returns**: `None`
  - **Parameters**:
    - #### `file`
      - **Type**: `str`
      - **Default**: ***REQUIRED***
      - **Description**: The path to the file to save the log node to.
      - **Example**: `my_log_node`
      - **Note**: Supports relative and absolute paths, also add `.lgnd` to the end of the file name.

### `enable`  
  - **Description**: Enables the log node.
  - **Returns**: `None`
  - **Parameters**: `None`
  - **Note**: If the log node is already enabled, this method does nothing, this is shorthand for `lognode.enabled = True`.

### `disable`
  - **Description**: Disables the log node.
  - **Returns**: `None`
  - **Parameters**: `None`
  - **Note**: If the log node is already disabled, this method does nothing. This is shorthand for `lognode.enabled = False`.

### dunders

 - #### `__repr__`
    - **Description**: Returns a string representation of the log node.
    - **Returns**: `str`
    - **Example**: `LogNode example at output console`, `LogNode example at output log.log`

 - #### `__len__`
    - **Description**: Returns the number of messages in memory.
    - **Returns**: `int`
    - **Example**: `10`

 - #### `__getitem__`
    - **Description**: Returns the message at the index.
    - **Returns**: `LogMessage`
    - **Parameters**:
      - #### `index`
        - **Type**: `int`
        - **Default**: ***REQUIRED***
        - **Description**: The index of the message to retrieve.
        - **Example**: `0`
 - #### `__contains__`
    - **Description**: Checks if the log node has a specific message.
    - **Returns**: `bool`
    - **Parameters**:
      - #### `message`
        - **Type**: `LogMessage`
        - **Default**: ***REQUIRED***
        - **Description**: The message to check for.
        - **Example**: `Error, Warn, Info`
        - **Note**: Does not work with exceptions.
- #### `__iter__`
    - **Description**: Iterates through the messages in memory.
    - **Returns**: `LogMessage` (per iteration)
    - **Example**: `for message in lognode: print(message)`
  