"""miscellaneous utility functions for your convenience"""
from objlog import LogNode
import traceback


def monitor(log_node: LogNode, raise_exceptions: bool = False):
    """a decorator to monitor a function and log any python exceptions that occur"""
    def decorator(func):
        """
        :param func:
        :return:
        """
        def wrapper(*args, **kwargs):
            """
            :param args:
            :param kwargs:
            :return:
            """
            try:
                return func(*args, **kwargs)
            except Exception as e:
                log_node.log(e)
                if raise_exceptions:
                    # clean up the exception message and raise it
                    # edit the traceback to remove the decorator's stack frame
                    e.__traceback__ = e.__traceback__.tb_next
                    raise e
                    # this is required to prevent the code from continuing to run after the exception is raised
                    # noinspection PyUnreachableCode
                    exit(1)

        return wrapper

    return decorator
