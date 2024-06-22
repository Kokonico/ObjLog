"""test the functionality of the logger"""

import unittest
import random
import os
import datetime
import os
import subprocess

from objlog import LogNode, LogMessage, utils
from objlog.LogMessages import Debug, Info, Warn, Error, Fatal, PythonExceptionMessage

LOG_FOLDER = "logs"


class CustomMessage(LogMessage):
    color = "\033[0m"
    level = "CUSTOM"


def gen_random_messages(amount: int, extra_classes: list | None = None):
    """generate random messages"""
    messages = []
    if extra_classes is None:
        extra_classes = []
    for i in range(amount):
        messages.append(random.choice([Debug, Info, Warn, Error, Fatal] + extra_classes)("This is a random message"))
    return messages


class TestLogNode(unittest.TestCase):
    """test the LogNode class"""

    @classmethod
    def setUpClass(cls):
        """Create a LogNode instance for all tests in this class"""
        cls.log = LogNode(name="Test", log_file=os.path.join(LOG_FOLDER, "LogNodeTest.log"), log_when_closed=False)
        cls.log2 = LogNode(name="Test2", log_file=os.path.join(LOG_FOLDER, "LogNodeTest2.log"), log_when_closed=False)
        cls.log_at_console = LogNode(name="Test", print_to_console=True)
        cls.log_at_none = LogNode(name="Test")

    def tearDown(self):
        """Clear the log after each test"""
        self.log.wipe_messages(wipe_logfiles=True)  # wipe messages and logfiles
        self.log2.wipe_messages(wipe_logfiles=True)  # wipe messages and logfiles
        self.log_at_console.wipe_messages(wipe_logfiles=True)  # wipe messages and logfiles
        self.log_at_none.wipe_messages(wipe_logfiles=True)  # wipe messages and logfiles

    # kinda essential tests

    def test_lognode_wipe_messages(self):
        messages = gen_random_messages(100, extra_classes=[CustomMessage])
        for message in messages:
            self.log.log(message)
        self.log.wipe_messages()
        self.assertEqual(0, len(self.log))
        # make sure log file is still there with all messages.
        with open(self.log.log_file) as f:
            self.assertEqual(100, len(f.readlines()))
        self.tearDown()

    def test_lognode_clear_logfile(self):
        messages = gen_random_messages(100, extra_classes=[CustomMessage])
        for message in messages:
            self.log.log(message)
        self.log.clear_log()
        # make sure messages are still there in memory
        self.assertEqual(100, len(self.log))
        # make sure log file is still there with no messages.
        with open(self.log.log_file) as f:
            self.assertEqual(0, len(f.readlines()))
        self.tearDown()

    def test_lognode_wipe_messages_and_logfiles(self):
        messages = gen_random_messages(100, extra_classes=[CustomMessage])
        for message in messages:
            self.log.log(message)
        self.log.wipe_messages(wipe_logfiles=True)
        # make sure messages are not there in memory
        self.assertEqual(0, len(self.log))
        # make sure log file is still there with no messages.
        with open(self.log.log_file) as f:
            self.assertEqual(0, len(f.readlines()))
        self.tearDown()

    # dunder methods

    def test_lognode_len(self):
        messages = gen_random_messages(100)
        for message in messages:
            self.log.log(message)
        self.assertEqual(100, len(self.log))
        self.tearDown()

    def test_lognode_getitem(self):
        messages = gen_random_messages(100)
        for message in messages:
            self.log.log(message)
        self.assertEqual(messages[0], self.log[0])
        self.tearDown()

    # no setitem dunder, because that's not how logs work!

    def test_lognode_iter(self):
        messages = gen_random_messages(100)
        for message in messages:
            self.log.log(message)
        for message in self.log:
            self.assertTrue(message in messages)
        self.tearDown()

    def test_lognode_contains(self):
        messages = gen_random_messages(100)
        for message in messages:
            self.log.log(message)
        self.assertTrue(messages[0] in self.log)
        self.tearDown()

    def test_lognode_repr(self):
        # just for this, we're going to create some lognodes with different parameters
        self.assertEqual(f"LogNode Test at output {os.path.join(LOG_FOLDER, 'LogNodeTest.log')}", repr(self.log))
        self.assertEqual("LogNode Test at output console", repr(self.log_at_console))
        self.assertEqual("LogNode Test at output None", repr(self.log_at_none))
        self.tearDown()

    # no more dunder methods

    def test_lognode_creation(self):
        self.assertTrue(isinstance(self.log, LogNode))

    def test_lognode_log(self):
        # create messages and set to a variable
        debug = Debug("This is a debug message")
        info = Info("This is an info message")
        warn = Warn("This is a warning message")
        error = Error("This is an error message")
        fatal = Fatal("This is a fatal message")

        # log the messages
        self.log.log(debug)
        self.log.log(info)
        self.log.log(warn)
        self.log.log(error)
        self.log.log(fatal)

        self.assertEqual(5, len(self.log))
        self.assertListEqual(self.log.get(
            Debug, Info, Warn, Error, Fatal),
            [debug, info, warn, error, fatal]
        )
        self.tearDown()  # NOTE: this is necessary because the log file is not cleared after each test,
        # so the next test might have unexpected results if this is not called.

    def test_lognode_get(self):
        messages = gen_random_messages(100, extra_classes=[CustomMessage])
        for message in messages:
            self.log.log(message)
        self.assertListEqual(self.log.get(), messages)
        self.tearDown()

    def test_lognode_get_filtered(self):
        messages = gen_random_messages(100, extra_classes=[CustomMessage])
        for message in messages:
            self.log.log(message)
        for message in self.log.get(CustomMessage):
            self.assertTrue(isinstance(message, CustomMessage))
        self.tearDown()

    def test_lognode_get_filtered_python_exceptions(self):
        self.log.log(ImportError("this is an ImportError"))
        self.log.log(ZeroDivisionError("this is a ZeroDivisionError"))
        self.log.log(NotImplementedError("this is a NotImplementedError"))
        self.log.log(RecursionError("this is a RecursionError"))
        self.log.log(KeyboardInterrupt("this is a KeyboardInterrupt"))
        self.log.log(EOFError("this is an EOFError"))
        self.log.log(StopIteration("this is a StopIteration"))
        self.log.log(GeneratorExit("this is a GeneratorExit"))
        self.log.log(SystemExit("this is a SystemExit"))
        self.log.log(SystemError("this is a SystemError"))
        self.log.log(Warning("this is a Warning"))
        self.log.log(CustomMessage("this is a CustomMessage"))
        self.log.log(Debug("this is a Debug message"))
        self.log.log(Info("this is an Info message"))
        self.log.log(Warn("this is a Warn message"))
        self.log.log(Error("this is an Error message"))
        self.log.log(Fatal("this is a Fatal message"))
        self.assertEqual(3, len(self.log.get(ImportError, ZeroDivisionError, CustomMessage)))
        self.tearDown()

    def test_lognode_log_multiple(self):
        messages = gen_random_messages(100, extra_classes=[CustomMessage])
        for message in messages:
            self.log.log(message)
        self.assertEqual(100, len(self.log))
        self.assertListEqual(self.log.get(), messages)
        self.tearDown()

    def test_lognode_squash(self):
        squash_message = Debug("squashed!")
        messages = gen_random_messages(100, extra_classes=[CustomMessage])
        for message in messages:
            self.log.log(message)
        self.log.squash(squash_message)
        self.assertEqual(squash_message, self.log[0])  # check that the first message is the squash message
        self.tearDown()

    def test_lognode_combine(self):
        messages = gen_random_messages(100, extra_classes=[CustomMessage])
        for message in messages:
            self.log.log(message)
        self.log2.combine(self.log)
        self.assertEqual(100, len(self.log2))
        self.assertListEqual(self.log2.get(), messages)
        self.tearDown()
        # now test with messages in both lognodes
        messages1 = gen_random_messages(100)
        messages2 = gen_random_messages(100)
        for message in messages1:
            self.log.log(message)
        for message in messages2:
            self.log2.log(message)

        self.log2.combine(self.log)

        self.assertEqual(200, len(self.log2))
        self.tearDown()

    def test_lognode_init_max_messages(self):
        log = LogNode(name="Test", max_messages_in_memory=10)
        self.assertEqual(10, log.max)
        self.assertEqual(10, log.messages.maxlen)
        self.tearDown()
        del log

    def test_lognode_init_max_log_size(self):
        log = LogNode(name="Test", max_log_messages=10, log_file=os.path.join(LOG_FOLDER, "LogNodeTest.log"))
        # add 100 messages
        messages = gen_random_messages(100)
        for message in messages:
            log.log(message)
        # check that the log file has 10 messages
        with open(os.path.join(LOG_FOLDER, "LogNodeTest.log")) as f:
            self.assertEqual(10, len(f.readlines()))
        del log
        self.tearDown()

    def test_lognode_set_max_messages(self):
        log = LogNode(name="Test", max_messages_in_memory=10)
        # log 100 messages
        messages = gen_random_messages(100)
        for message in messages:
            log.log(message)
        # check that the log has 10 messages
        self.assertEqual(10, len(log))
        log.set_max_messages_in_memory(20)
        self.assertEqual(10, len(log))
        # log 100 messages
        messages = gen_random_messages(100)
        for message in messages:
            log.log(message)
        self.assertEqual(20, len(log))

        # now truncate the log to 10 messages

        log.set_max_messages_in_memory(10)
        self.assertEqual(10, len(log))

        self.tearDown()
        del log

    def test_lognode_set_max_log_size(self):
        log = LogNode(name="Test", max_log_messages=10, log_file=os.path.join(LOG_FOLDER, "LogNodeTest.log"))
        # log 100 messages
        messages = gen_random_messages(100)
        for message in messages:
            log.log(message)
        # check that the log file has 10 messages
        with open(os.path.join(LOG_FOLDER, "LogNodeTest.log")) as f:
            self.assertEqual(10, len(f.readlines()))

        # now set the max log size to 20
        log.set_max_messages_in_log(20)

        with open(os.path.join(LOG_FOLDER, "LogNodeTest.log")) as f:
            self.assertEqual(10, len(f.readlines()))
        # log 100 messages
        messages = gen_random_messages(100)
        for message in messages:
            log.log(message)
        with open(os.path.join(LOG_FOLDER, "LogNodeTest.log")) as f:
            self.assertEqual(20, len(f.readlines()))

        # now truncate the log to 10 messages

        log.set_max_messages_in_log(10)
        with open(os.path.join(LOG_FOLDER, "LogNodeTest.log")) as f:
            self.assertEqual(10, len(f.readlines()))

        del log
        self.tearDown()

    def test_lognode_set_max_log_size_and_max_messages(self):
        log = LogNode(name="Test", max_log_messages=10, max_messages_in_memory=10,
                      log_file=os.path.join(LOG_FOLDER, "LogNodeTest.log"))
        # log 100 messages
        messages = gen_random_messages(100)
        for message in messages:
            log.log(message)
        # check that the log file has 10 messages
        with open(os.path.join(LOG_FOLDER, "LogNodeTest.log")) as f:
            self.assertEqual(10, len(f.readlines()))

        # now set the max log size to 20
        log.set_max_messages_in_log(20)

        with open(os.path.join(LOG_FOLDER, "LogNodeTest.log")) as f:
            self.assertEqual(10, len(f.readlines()))
        # log 100 messages
        messages = gen_random_messages(100)
        for message in messages:
            log.log(message)
        with open(os.path.join(LOG_FOLDER, "LogNodeTest.log")) as f:
            self.assertEqual(20, len(f.readlines()))

        # now truncate the log to 10 messages

        log.set_max_messages_in_log(10)
        with open(os.path.join(LOG_FOLDER, "LogNodeTest.log")) as f:
            self.assertEqual(10, len(f.readlines()))

        del log
        self.tearDown()

    # filter tests

    def test_lognode_filter(self):
        messages = gen_random_messages(100, extra_classes=[CustomMessage])
        for message in messages:
            self.log.log(message)
        # filter out all messages that are not CustomMessage
        self.log.filter([CustomMessage])
        for message in self.log:
            self.assertTrue(isinstance(message, CustomMessage))
        self.tearDown()

    def test_lognode_filter_multiple(self):
        messages = gen_random_messages(100, extra_classes=[CustomMessage])
        for message in messages:
            self.log.log(message)
        # filter out all messages that are not CustomMessage
        self.log.filter([CustomMessage, Debug])
        for message in self.log:
            self.assertTrue(isinstance(message, CustomMessage) or isinstance(message, Debug))
        self.tearDown()

    def test_lognode_filter_python_exceptions(self):
        self.log.log(ImportError("this is an ImportError"))
        self.log.log(ZeroDivisionError("this is a ZeroDivisionError"))
        self.log.log(NotImplementedError("this is a NotImplementedError"))

        self.log.filter([ImportError, ZeroDivisionError])

    def test_lognode_dump(self):
        messages = gen_random_messages(100, extra_classes=[CustomMessage])
        for message in messages:
            self.log.log(message)
        self.log.clear_log()  # very important, otherwise the log file will be appended to
        self.log.dump_messages(f"{os.path.join(LOG_FOLDER, 'LogNodeTest.log')}")
        with open(os.path.join(LOG_FOLDER, "LogNodeTest.log")) as f:
            self.assertEqual(100, len(f.readlines()))
        self.tearDown()

    def test_lognode_dump_memory(self):
        messages = gen_random_messages(100, extra_classes=[CustomMessage])
        for message in messages:
            self.log.log(message)
        self.log.clear_log()
        self.log.dump_messages(f"{os.path.join(LOG_FOLDER, 'LogNodeTest.log')}", wipe_messages_from_memory=True)
        with open(os.path.join(LOG_FOLDER, "LogNodeTest.log")) as f:
            self.assertEqual(100, len(f.readlines()))
        self.assertEqual(0, len(self.log))
        self.tearDown()

    def test_lognode_dump_filtered(self):
        messages = gen_random_messages(100, extra_classes=[CustomMessage])
        for message in messages:
            self.log.log(message)
        self.log.clear_log()
        self.log.dump_messages(f"{os.path.join(LOG_FOLDER, 'LogNodeTest.log')}", CustomMessage)
        with open(os.path.join(LOG_FOLDER, "LogNodeTest.log")) as f:
            for line in f.readlines():
                self.assertEqual("CUSTOM:", line.split(" ")[2])
        self.tearDown()

    def test_lognode_dump_filtered_multiple(self):
        messages = gen_random_messages(100, extra_classes=[CustomMessage])
        for message in messages:
            self.log.log(message)
        self.log.clear_log()
        self.log.dump_messages(f"{os.path.join(LOG_FOLDER, 'LogNodeTest.log')}", CustomMessage, Debug)
        with open(os.path.join(LOG_FOLDER, "LogNodeTest.log")) as f:
            for line in f.readlines():
                self.assertTrue(line.split(" ")[2] in ["CUSTOM:", "DEBUG:"])
        self.tearDown()

    def test_lognode_set_output_file(self):
        messages = gen_random_messages(100, extra_classes=[CustomMessage])
        for message in messages:
            self.log.log(message)
        self.log.set_output_file(os.path.join(LOG_FOLDER, "LogNodeTest2.log"))
        with open(os.path.join(LOG_FOLDER, "LogNodeTest2.log")) as f:
            self.assertEqual(0, len(f.readlines()))
        with open(os.path.join(LOG_FOLDER, "LogNodeTest.log")) as f:
            self.assertEqual(100, len(f.readlines()))

        self.log.log(messages[0])
        with open(os.path.join(LOG_FOLDER, "LogNodeTest2.log")) as f:
            self.assertEqual(1, len(f.readlines()))
        # set the log file back to the original
        self.log.set_output_file(os.path.join(LOG_FOLDER, "LogNodeTest.log"))
        self.tearDown()

    def test_lognode_set_output_file_preserve(self):
        messages = gen_random_messages(100, extra_classes=[CustomMessage])
        for message in messages:
            self.log.log(message)
        self.log.set_output_file(os.path.join(LOG_FOLDER, "LogNodeTest2.log"), preserve_old_messages=True)
        with open(os.path.join(LOG_FOLDER, "LogNodeTest2.log")) as f:
            self.assertEqual(100, len(f.readlines()))
        with open(os.path.join(LOG_FOLDER, "LogNodeTest.log")) as f:
            self.assertEqual(100, len(f.readlines()))

        self.log.log(messages[0])
        with open(os.path.join(LOG_FOLDER, "LogNodeTest2.log")) as f:
            self.assertEqual(101, len(f.readlines()))
        # set the log file back to the original
        self.log.set_output_file(os.path.join(LOG_FOLDER, "LogNodeTest.log"))
        self.tearDown()

    def test_lognode_set_output_file_preserve_and_wipe(self):
        messages = gen_random_messages(100, extra_classes=[CustomMessage])
        for message in messages:
            self.log.log(message)
        self.log.set_output_file(os.path.join(LOG_FOLDER, "LogNodeTest2.log"), preserve_old_messages=True)
        with open(os.path.join(LOG_FOLDER, "LogNodeTest2.log")) as f:
            self.assertEqual(100, len(f.readlines()))
        with open(os.path.join(LOG_FOLDER, "LogNodeTest.log")) as f:
            self.assertEqual(100, len(f.readlines()))

        self.log.log(messages[0])
        with open(os.path.join(LOG_FOLDER, "LogNodeTest2.log")) as f:
            self.assertEqual(101, len(f.readlines()))
        # set the log file back to the original
        self.log.set_output_file(os.path.join(LOG_FOLDER, "LogNodeTest.log"), preserve_old_messages=True)
        self.tearDown()

    def test_has_errors_method(self):
        self.log.log(Info("this is an info message"))
        self.log.log(Error("this is an error message"))
        self.assertTrue(self.log.has_errors())
        self.tearDown()
        self.log.log(Info("this is an info message"))
        self.log.log(Warn("this is a warning message"))
        self.assertFalse(self.log.has_errors())
        self.tearDown()
        self.assertFalse(self.log.has_errors())

    def test_has_method(self):
        self.log.log(Info("this is an info message"))
        self.log.log(Warn("this is a warning message"))
        self.assertTrue(self.log.has(Warn))
        self.tearDown()
        self.log.log(Info("this is an info message"))
        self.log.log(Warn("this is a warning message"))
        self.assertFalse(self.log.has(Error))
        self.tearDown()
        self.assertFalse(self.log.has(Fatal))

    def test_logging_default_python_exceptions(self):
        self.log.log(ImportError("this is an ImportError"))
        self.log.log(ZeroDivisionError("this is a ZeroDivisionError"))
        self.log.log(NotImplementedError("this is a NotImplementedError"))
        self.log.log(RecursionError("this is a RecursionError"))
        self.log.log(KeyboardInterrupt("this is a KeyboardInterrupt"))
        self.log.log(EOFError("this is an EOFError"))
        self.log.log(StopIteration("this is a StopIteration"))
        self.log.log(GeneratorExit("this is a GeneratorExit"))
        self.log.log(SystemExit("this is a SystemExit"))
        self.log.log(SystemError("this is a SystemError"))
        self.log.log(Warning("this is a Warning"))
        self.tearDown()

    def test_logging_custom_python_exceptions(self):
        class CustomException(Exception):
            pass
        self.log.log(CustomException("this is a CustomException"))
        self.tearDown()

    def test_logging_real_exception(self):
        try:
            raise Exception("this is a real exception")
        except Exception as e:
            self.log.log(e)
        self.tearDown()

    def test_has_errors_on_real_exception(self):
        try:
            raise Exception("this is a real exception")
        except Exception as e:
            self.log.log(e)
        self.assertTrue(self.log.has_errors())
        self.tearDown()

    def test_has_on_python_exception(self):
        self.log.log(ImportError("this is an ImportError"))
        self.assertTrue(self.log.has(ImportError))
        self.tearDown()

    def test_get_on_python_exception(self):
        self.log.log(ImportError("this is an ImportError"))
        self.assertTrue(isinstance(self.log.get(ImportError)[0], PythonExceptionMessage))
        self.assertTrue(isinstance(self.log.get(ImportError)[0].exception, ImportError))
        self.tearDown()

    def test_monitor_decorator(self):
        @utils.monitor(self.log)
        def test_function():
            raise Exception("this is a real exception")

        test_function()
        self.assertTrue(self.log.has_errors())
        self.tearDown()

    def test_monitor_decorator_raise_on_exception(self):
        @utils.monitor(self.log, raise_exceptions=True)
        def test_function():
            raise Exception("this is a real exception")

        with self.assertRaises(Exception):
            test_function()
        self.tearDown()

    def test_monitor_decorator_exit_on_exception(self):
        @utils.monitor(self.log, exit_on_exception=True)
        def test_function():
            raise Exception("this is a real exception")

        with self.assertRaises(SystemExit):
            test_function()
        self.tearDown()

    def test_rename_log_node(self):
        old_name = self.log.name

        # log some messages

        messages = gen_random_messages(100, extra_classes=[CustomMessage])
        for message in messages:
            self.log.log(message)

        self.log.rename("NewName")
        self.assertEqual("NewName", self.log.name)
        # check all messages for old name
        with open(self.log.log_file) as f:
            lines = f.readlines()
            for line in lines:
                self.assertTrue(old_name in line)

        # log some more messages

        messages = gen_random_messages(100, extra_classes=[CustomMessage])

        for message in messages:
            self.log.log(message)

        # check last 100 messages

        with open(self.log.log_file) as f:
            lines = f.readlines()
            # check if the last 100 messages are from the new name
            for line in lines[-100:]:
                self.assertTrue("NewName" in line)


        self.log.rename("Test")  # revert to the original name (for other tests)
        self.tearDown()


class TestLogMessage(unittest.TestCase):
    """
    test the LogMessage class
    (NOTICE, ALL OF THESE TESTS WILL BE DONE WITH CHILD CLASSES.
    THIS IS BECAUSE LogMessage IS NOT MEANT TO BE USED ALONE)
    """

    def test_builtins_are_logmessages(self):
        self.assertTrue(isinstance(Debug("test"), LogMessage))
        self.assertTrue(isinstance(Info("test"), LogMessage))
        self.assertTrue(isinstance(Warn("test"), LogMessage))
        self.assertTrue(isinstance(Error("test"), LogMessage))
        self.assertTrue(isinstance(Fatal("test"), LogMessage))
        self.assertTrue(isinstance(PythonExceptionMessage(Exception("test")), LogMessage))
        self.tearDown()

    def test_custom_class_is_logmessage(self):
        self.assertTrue(isinstance(CustomMessage("test"), LogMessage))
        self.tearDown()

    def test_logmessage_colored(self):
        messages = gen_random_messages(100, extra_classes=[CustomMessage])
        for message in messages:
            self.assertTrue(isinstance(message.colored(), str))
            dt = datetime.datetime.fromtimestamp(message.unix / 1000)
            # shave ms to 3 decimal places
            dt = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            self.assertEqual(
                f"{message.color}[{dt}] {message.level}: {message.message}\033[0m",
                message.colored()
            )

    def test_logmessage_str(self):
        messages = gen_random_messages(100, extra_classes=[CustomMessage])
        for message in messages:
            self.assertTrue(isinstance(str(message), str))
            dt = datetime.datetime.fromtimestamp(message.unix / 1000)
            self.assertEqual(f"[{dt}] {message.level}: {message.message}", str(message))

    def test_logmessage_repr(self):
        messages = gen_random_messages(100, extra_classes=[CustomMessage])
        for message in messages:
            self.assertTrue(isinstance(repr(message), str))
            self.assertEqual(f"{message.level}: {message.message}", repr(message))

    def test_logmessage_individuality(self):
        message_A = gen_random_messages(1, extra_classes=[CustomMessage])[0]
        message_B = gen_random_messages(1, extra_classes=[CustomMessage])[0]
        self.assertNotEqual(message_A, message_B)
        message_A = Debug("test")
        message_B = Debug("test")
        self.assertNotEqual(message_A, message_B)

        message_A = CustomMessage("test")
        message_B = CustomMessage("test")
        self.assertNotEqual(message_A, message_B)

        message_A = CustomMessage("test")
        message_B = Debug("test")

        self.assertNotEqual(message_A, message_B)

        message_A = CustomMessage("test")
        message_B = message_A
        self.assertEqual(message_A, message_B)


class TestRunExamples(unittest.TestCase):
    # run all files in the examples folder
    def test_run_examples(self):
        # check if the examples folder exists
        if not os.path.exists("examples"):
            # cd ..
            os.chdir("..")
            # check again
            if not os.path.exists("examples"):
                self.fail("examples folder does not exist")
        # enter the examples folder (if not already there)
        if os.getcwd().split(os.path.sep)[-1] != "examples":
            os.chdir("examples")
        # check if the log folder exists
        if not os.path.exists(LOG_FOLDER):
            os.mkdir(LOG_FOLDER)
        # move to the log folder
        os.chdir(LOG_FOLDER)
        for file in os.listdir():
            if file.endswith(".py"):
                try:
                    subprocess.run(["python", os.path.join("..", file)])
                except Exception as e:
                    self.fail(f"failed to run {file} with error: {e}")
        # if no errors are raised, the tests pass
        self.assertTrue(True)
