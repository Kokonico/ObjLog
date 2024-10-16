# Utils

## @monitor
- **Type**: Decorator
- **Description**: Monitor a function, if a python exception is raised, it will be logged, and the function will return None.
- **Parameters**:
  - `log_node`
    - **Type**: `LogNode`
    - **Default**: ***Required***
    - **Description**: The log node to use for logging any exceptions that occur.
  - `raise_exceptions`
    - **Type**: `bool`
    - **Default**: `False`
    - **Description**: If True, the exception will be raised after logging. If False, the exception will be suppressed.
 - `exit_on_exception`
    - **Type**: `bool`
    - **Default**: `False`
    - **Description**: If True, the program will raise a SystemExit after logging the exception. If False, the program will continue running.
    - **Note**: This parameter overrides `raise_exceptions` and will always close the program if an exception is raised without raising it.
    Also, this parameter is not recommended for internal code, and should only be used in user-facing code.
