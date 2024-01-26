"""test the functionality of the logger"""

import unittest
import random
import os

from objlog import LogNode, LogMessage
from objlog.LogMessages import Debug, Info, Warn, Error, Fatal

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
        self.assertEqual(len(self.log), 0)
        # make sure log file is still there with all messages.
        with open(self.log.log_file) as f:
            self.assertEqual(len(f.readlines()), 100)
        self.tearDown()

    def test_lognode_clear_logfile(self):
        messages = gen_random_messages(100, extra_classes=[CustomMessage])
        for message in messages:
            self.log.log(message)
        self.log.clear_log()
        # make sure messages are still there in memory
        self.assertEqual(len(self.log), 100)
        # make sure log file is still there with no messages.
        with open(self.log.log_file) as f:
            self.assertEqual(len(f.readlines()), 0)
        self.tearDown()

    def test_lognode_wipe_messages_and_logfiles(self):
        messages = gen_random_messages(100, extra_classes=[CustomMessage])
        for message in messages:
            self.log.log(message)
        self.log.wipe_messages(wipe_logfiles=True)
        # make sure messages are not there in memory
        self.assertEqual(len(self.log), 0)
        # make sure log file is still there with no messages.
        with open(self.log.log_file) as f:
            self.assertEqual(len(f.readlines()), 0)
        self.tearDown()

    # dunder methods

    def test_lognode_len(self):
        messages = gen_random_messages(100)
        for message in messages:
            self.log.log(message)
        self.assertEqual(len(self.log), 100)
        self.tearDown()

    def test_lognode_getitem(self):
        messages = gen_random_messages(100)
        for message in messages:
            self.log.log(message)
        self.assertEqual(self.log[0], messages[0])
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
        self.assertEqual(repr(self.log), f"LogNode Test at output {os.path.join(LOG_FOLDER, 'LogNodeTest.log')}")
        self.assertEqual(repr(self.log_at_console), "LogNode Test at output console")
        self.assertEqual(repr(self.log_at_none), "LogNode Test at output None")
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

        self.assertEqual(len(self.log), 5)
        self.assertListEqual(self.log.get(
            element_filter=[Debug, Info, Warn, Error, Fatal]),
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
        for message in self.log.get(element_filter=[CustomMessage]):
            self.assertTrue(isinstance(message, CustomMessage))
        self.tearDown()

    def test_lognode_log_multiple(self):
        messages = gen_random_messages(100, extra_classes=[CustomMessage])
        for message in messages:
            self.log.log(message)
        self.assertEqual(len(self.log), 100)
        self.assertListEqual(self.log.get(), messages)
        self.tearDown()

    def test_lognode_squash(self):
        squash_message = Debug("squashed!")
        messages = gen_random_messages(100, extra_classes=[CustomMessage])
        for message in messages:
            self.log.log(message)
        self.log.squash(squash_message)
        self.assertEqual(self.log[0], squash_message)  # check that the first message is the squash message
        self.tearDown()

    def test_lognode_combine(self):
        messages = gen_random_messages(100, extra_classes=[CustomMessage])
        for message in messages:
            self.log.log(message)
        self.log2.combine(self.log)
        self.assertEqual(len(self.log2), 100)
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

        self.assertEqual(len(self.log2), 200)
        self.tearDown()

    def test_lognode_init_max_messages(self):
        log = LogNode(name="Test", max_messages_in_memory=10)
        self.assertEqual(log.max, 10)
        self.assertEqual(log.messages.maxlen, 10)
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
            self.assertEqual(len(f.readlines()), 10)
        del log
        self.tearDown()

    def test_lognode_set_max_messages(self):
        log = LogNode(name="Test", max_messages_in_memory=10)
        # log 100 messages
        messages = gen_random_messages(100)
        for message in messages:
            log.log(message)
        # check that the log has 10 messages
        self.assertEqual(len(log), 10)
        log.set_max_messages_in_memory(20)
        self.assertEqual(len(log), 10)
        # log 100 messages
        messages = gen_random_messages(100)
        for message in messages:
            log.log(message)
        self.assertEqual(len(log), 20)

        # now truncate the log to 10 messages

        log.set_max_messages_in_memory(10)
        self.assertEqual(len(log), 10)

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
            self.assertEqual(len(f.readlines()), 10)

        # now set the max log size to 20
        log.set_max_messages_in_log(20)

        with open(os.path.join(LOG_FOLDER, "LogNodeTest.log")) as f:
            self.assertEqual(len(f.readlines()), 10)
        # log 100 messages
        messages = gen_random_messages(100)
        for message in messages:
            log.log(message)
        with open(os.path.join(LOG_FOLDER, "LogNodeTest.log")) as f:
            self.assertEqual(len(f.readlines()), 20)

        # now truncate the log to 10 messages

        log.set_max_messages_in_log(10)
        with open(os.path.join(LOG_FOLDER, "LogNodeTest.log")) as f:
            self.assertEqual(len(f.readlines()), 10)

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

    def test_lognode_dump(self):
        messages = gen_random_messages(100, extra_classes=[CustomMessage])
        for message in messages:
            self.log.log(message)
        self.log.clear_log()  # very important, otherwise the log file will be appended to
        self.log.dump_messages(f"{os.path.join(LOG_FOLDER, 'LogNodeTest.log')}")
        with open(os.path.join(LOG_FOLDER, "LogNodeTest.log")) as f:
            self.assertEqual(len(f.readlines()), 100)
        self.tearDown()

    def test_lognode_dump_memory(self):
        messages = gen_random_messages(100, extra_classes=[CustomMessage])
        for message in messages:
            self.log.log(message)
        self.log.clear_log()
        self.log.dump_messages(f"{os.path.join(LOG_FOLDER, 'LogNodeTest.log')}", wipe_messages_from_memory=True)
        with open(os.path.join(LOG_FOLDER, "LogNodeTest.log")) as f:
            self.assertEqual(len(f.readlines()), 100)
        self.assertEqual(len(self.log), 0)
        self.tearDown()

    def test_lognode_dump_filtered(self):
        messages = gen_random_messages(100, extra_classes=[CustomMessage])
        for message in messages:
            self.log.log(message)
        self.log.clear_log()
        self.log.dump_messages(f"{os.path.join(LOG_FOLDER, 'LogNodeTest.log')}", [CustomMessage])
        with open(os.path.join(LOG_FOLDER, "LogNodeTest.log")) as f:
            for line in f.readlines():
                self.assertEqual(line.split(" ")[2], "CUSTOM:")
        self.tearDown()

    def test_lognode_dump_filtered_multiple(self):
        messages = gen_random_messages(100, extra_classes=[CustomMessage])
        for message in messages:
            self.log.log(message)
        self.log.clear_log()
        self.log.dump_messages(f"{os.path.join(LOG_FOLDER, 'LogNodeTest.log')}", [CustomMessage, Debug])
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
            self.assertEqual(len(f.readlines()), 0)
        with open(os.path.join(LOG_FOLDER, "LogNodeTest.log")) as f:
            self.assertEqual(len(f.readlines()), 100)

        self.log.log(messages[0])
        with open(os.path.join(LOG_FOLDER, "LogNodeTest2.log")) as f:
            self.assertEqual(len(f.readlines()), 1)
        # set the log file back to the original
        self.log.set_output_file(os.path.join(LOG_FOLDER, "LogNodeTest.log"))
        self.tearDown()

    def test_lognode_set_output_file_preserve(self):
        messages = gen_random_messages(100, extra_classes=[CustomMessage])
        for message in messages:
            self.log.log(message)
        self.log.set_output_file(os.path.join(LOG_FOLDER, "LogNodeTest2.log"), preserve_old_messages=True)
        with open(os.path.join(LOG_FOLDER, "LogNodeTest2.log")) as f:
            self.assertEqual(len(f.readlines()), 100)
        with open(os.path.join(LOG_FOLDER, "LogNodeTest.log")) as f:
            self.assertEqual(len(f.readlines()), 100)

        self.log.log(messages[0])
        with open(os.path.join(LOG_FOLDER, "LogNodeTest2.log")) as f:
            self.assertEqual(len(f.readlines()), 101)
        # set the log file back to the original
        self.log.set_output_file(os.path.join(LOG_FOLDER, "LogNodeTest.log"))
        self.tearDown()

    def test_lognode_set_output_file_preserve_and_wipe(self):
        messages = gen_random_messages(100, extra_classes=[CustomMessage])
        for message in messages:
            self.log.log(message)
        self.log.set_output_file(os.path.join(LOG_FOLDER, "LogNodeTest2.log"), preserve_old_messages=True)
        with open(os.path.join(LOG_FOLDER, "LogNodeTest2.log")) as f:
            self.assertEqual(len(f.readlines()), 100)
        with open(os.path.join(LOG_FOLDER, "LogNodeTest.log")) as f:
            self.assertEqual(len(f.readlines()), 100)

        self.log.log(messages[0])
        with open(os.path.join(LOG_FOLDER, "LogNodeTest2.log")) as f:
            self.assertEqual(len(f.readlines()), 101)
        # set the log file back to the original
        self.log.set_output_file(os.path.join(LOG_FOLDER, "LogNodeTest.log"), preserve_old_messages=True)
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
        self.tearDown()

    def test_custom_class_is_logmessage(self):
        self.assertTrue(isinstance(CustomMessage("test"), LogMessage))
        self.tearDown()

    def test_logmessage_colored(self):
        messages = gen_random_messages(100, extra_classes=[CustomMessage])
        for message in messages:
            self.assertTrue(isinstance(message.colored(), str))
            self.assertEqual(message.colored(), f"{message.color}[{message.timestamp}] {message.level}: {message.message}\033[0m")

    def test_logmessage_str(self):
        messages = gen_random_messages(100, extra_classes=[CustomMessage])
        for message in messages:
            self.assertTrue(isinstance(str(message), str))
            self.assertEqual(str(message), f"[{message.timestamp}] {message.level}: {message.message}")

    def test_logmessage_repr(self):
        messages = gen_random_messages(100, extra_classes=[CustomMessage])
        for message in messages:
            self.assertTrue(isinstance(repr(message), str))
            self.assertEqual(repr(message), f"{message.level}: {message.message}")

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
