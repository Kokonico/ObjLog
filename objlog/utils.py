"""miscellaneous utility functions for your convenience"""
from objlog import LogNode
import traceback


def monitor(log_node: LogNode, exit_on_exception: bool = False, raise_exceptions: bool = False):
    """a decorator to monitor a function and log any python exceptions that occur"""
    def decorator(func):
        """
        :param func:
        :return:
        """
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # clean up the exception message and raise it
                # edit the traceback to remove the decorator's stack frame
                e.__traceback__ = e.__traceback__.tb_next
                log_node.log(e)
                if exit_on_exception:
                    # red color escape code
                    print("\033[91m", end="")
                    if log_node.print is False and log_node.log_file is not None:
                        print(f"An exception occurred: {e}, please check the log file for more information.")
                    # if log node prints to the console, no need to print the message again
                    # if lognode does not print to the console or save to a file,  print the stack trace to the console
                    if log_node.print is False and log_node.log_file is None:
                        print(f"An unhandled exception occurred: {e}")
                        print(traceback.format_exc())
                    print("\033[0m", end="")
                    exit(1)
                elif raise_exceptions:
                    raise e

        return wrapper
    return decorator