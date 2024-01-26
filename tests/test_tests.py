"""test the functionality of the logger"""

import unittest
import random
import os

from objlog import LogNode, LogMessage
from objlog.LogMessages import Debug, Info, Warn, Error, Fatal


def gen_random_messages(amount: int, extra_classes: list | None = None):
    """generate random messages"""
    messages = []
    if extra_classes is None:
        extra_classes = []
    for i in range(amount):
        messages.append(random.choice([Debug, Info, Warn, Error, Fatal] + extra_classes)("This is a random message"))
    return messages


class TestFilter(unittest.TestCase):
    """test the filtering functionality of the logger"""

    # new log node

    log = LogNode(name="Test", log_file="test.log", log_when_closed=False)  # so it doesn't log when closed, making

    # it easier to test.

    class CustomMessage(LogMessage):
        level = "CUSTOM"
        color = "\033[1;35m"  # purple

    def test_live_filter(self):

        # log 20 messages, all of them random

        for i in gen_random_messages(20, extra_classes=[self.CustomMessage]):
            self.log.log(i)

        self.log.filter([Debug])

        # use for loop to test the filter

        for message in self.log.get(element_filter=[Debug, Info, Warn, Error, Fatal,
                                                    self.CustomMessage]):  # get all the messages (to avoid
            # double-dipping)
            self.assertEqual(message.level, "DEBUG")

    def test_get_filter(self):
        """test the get() function's filter argument"""
        for i in gen_random_messages(20, extra_classes=[self.CustomMessage]):
            self.log.log(i)

        for message in self.log.get(element_filter=[Debug]):
            self.assertEqual(message.level, "DEBUG")

        for message in self.log.get(element_filter=[Info]):
            self.assertEqual(message.level, "INFO")

        for message in self.log.get(element_filter=[Warn]):
            self.assertEqual(message.level, "WARN")

        for message in self.log.get(element_filter=[Error]):
            self.assertEqual(message.level, "ERROR")

        for message in self.log.get(element_filter=[Fatal]):
            self.assertEqual(message.level, "FATAL")

        for message in self.log.get(element_filter=[self.CustomMessage]):
            self.assertEqual(message.level, "CUSTOM")

    def test_filter_logfiles(self):
        """test the filter_logfiles argument"""
        for i in gen_random_messages(20, extra_classes=[self.CustomMessage]):
            self.log.log(i)
        self.log.filter([Debug], filter_logfiles=True)
        with open("test.log") as f:
            for line in f.readlines():
                self.assertEqual(line.split(" ")[2], "DEBUG:")


# noinspection SpellCheckingInspection
class TestLogNode(unittest.TestCase):
    """test the LogNode class"""

    def test_lognode_creation(self):
        log = LogNode(name="Test")
        self.assertTrue(isinstance(log, LogNode))

    def test_lognode_deletion(self):
        log = LogNode(name="Test")
        del log
        self.assertRaises(NameError, lambda: log)

    def test_lognode_log(self):
        log = LogNode(name="Test")

        # create messages and set to a variable

        debug = Debug("This is a debug message")
        info = Info("This is an info message")
        warn = Warn("This is a warning message")
        error = Error("This is an error message")
        fatal = Fatal("This is a fatal message")

        # log the messages

        log.log(debug)
        log.log(info)
        log.log(warn)
        log.log(error)
        log.log(fatal)

        self.assertEqual(len(log), 5)
        self.assertListEqual(log.get(
            element_filter=[Debug, Info, Warn, Error, Fatal]),
            [debug, info, warn, error, fatal]
        )

    def test_lognode_limiter_init(self):
        log = LogNode(name="Test", max_log_messages=10, max_messages_in_memory=5, log_file="limiter.log")
        self.assertEqual(log.maxinf, 10)
        self.assertEqual(log.max, 5)

        # test the limiter (memory)

        for f in range(20):
            log.log(Debug("This is a debug message"))
        self.assertEqual(len(log), 5)

        # test the limiter (log file)

        with open("limiter.log") as f:
            self.assertEqual(len(f.readlines()), 10)

    def test_lognode_limiter_setter(self):
        log = LogNode(name="Test", max_log_messages=10, max_messages_in_memory=5, log_file="limiter2.log")

        self.assertEqual(log.maxinf, 10)
        self.assertEqual(log.max, 5)

        # log 20 messages

        for i in range(20):
            log.log(Debug("This is a debug message"))

        self.assertEqual(len(log), 5)

        # do the same for the log file

        with open("limiter2.log") as f:
            self.assertEqual(len(f.readlines()), 10)

        # change the limiters

        log.set_max_messages_in_memory(10)
        log.set_max_messages_in_log(20)

        self.assertEqual(log.maxinf, 20)
        self.assertEqual(log.max, 10)

        # log 50 messages

        for i in range(50):
            log.log(Debug("This is a debug message"))

        self.assertEqual(len(log), 10)

        # do the same for the log file

        with open("limiter2.log") as f:
            self.assertEqual(len(f.readlines()), 20)

    # noinspection SpellCheckingInspection
    def test_logfile_methods(self):
        log = LogNode(name="Test", log_file="testx.log")

        # log 20 messages

        for i in range(20):
            log.log(Debug("This is a debug message"))

        # dump the messages to a file

        log.dump_messages("dumpxx.log", elementfilter=[Debug, Info, Warn, Error, Fatal])

        # check if the messages are in the file

        with open("dumpxx.log") as f:
            self.assertEqual(len(f.readlines()), 20)

        # check if the messages are in memory

        self.assertEqual(len(log), 20)

        # wipe the messages from memory

        log.wipe_messages(wipe_logfiles=True)

        # check if the messages are wiped

        self.assertEqual(len(log), 0)

        # check if the messages are wiped from the log file

        with open("testx.log") as f:
            self.assertEqual(len(f.readlines()), 0)

        # log 20 messages

        for i in range(20):
            log.log(Debug("This is a debug message"))

        # dump the messages to a file

        log.dump_messages("dump2.log", elementfilter=[Debug, Info, Warn, Error, Fatal])

        # check if the messages are in the file

        with open("dump2.log") as f:
            self.assertEqual(len(f.readlines()), 20)

        # wipe the messages from memory

        log.wipe_messages()

        # check if the messages are wiped

        self.assertEqual(len(log), 0)

        # check if the messages are NOT wiped from the log file

        with open("testx.log") as f:
            self.assertEqual(len(f.readlines()), 20)

        # wipe the messages from the log file

        log.clear_log()

        # check if the messages are wiped from the log file

        with open("testx.log") as f:
            self.assertEqual(len(f.readlines()), 0)

    def test_lognode_set_output_file(self):
        log = LogNode(name="Test")

        # log 20 messages

        for i in range(20):
            log.log(Debug("This is a debug message"))

        # change the output file

        log.set_output_file("testy.log")

        # log a message

        log.log(Debug("This is a debug message"))

        # check if the message is in the file

        with open("testy.log") as f:
            self.assertEqual(len(f.readlines()), 1)

        # change the output file

        log.set_output_file("test2.log", preserve_old_messages=True)

        # check if all 21 messages are in the file

        with open("test2.log") as f:
            self.assertEqual(len(f.readlines()), 21)

    def test_lognode_combine(self):
        log = LogNode(name="Test", log_file="blagh.log")

        # log 20 messages

        for i in range(20):
            log.log(Debug("This is a debug message"))

        log2 = LogNode(name="Test2")

        # log 20 messages

        for i in range(20):
            log2.log(Debug("This is a debug message"))

        log.combine(log2)

        self.assertEqual(len(log), 40)  # check if the messages are combined

        # check if blagh.log has 40 lines

        with open("blagh.log") as f:
            self.assertEqual(len(f.readlines()), 40)

    def test_lognode_combine_no_log_join(self):
        log = LogNode(name="Test", log_file="blagh2.log")
        log2 = LogNode(name="Test2", log_file="blagh3.log")

        # log 20 messages

        for i in range(20):
            log.log(Debug("This is a debug message"))

        # log 20 messages

        for i in range(20):
            log2.log(Debug("This is a debug message"))

        log.combine(log2, merge_log_files=False)

        self.assertEqual(len(log), 40)  # check if the messages are combined

        # check if blagh2.log has 20 lines

        with open("blagh2.log") as f:
            self.assertEqual(len(f.readlines()), 20)

    def test_LogNode_contains(self):
        """test the __contains__ method"""
        log = LogNode(name="Test", log_file="blagh4.log")

        # log 20 messages

        for i in range(20):
            log.log(Debug("This is a debug message"))

        message = Debug("This is a special debug message")

        log.log(message)

        self.assertTrue(message in log)
        self.assertFalse(Debug("This is a special debug message") in log)  # different object, same message.

    def test_LogNode_squash(self):
        """test the squash method"""
        log = LogNode(name="Test", log_file="blagh5.log")

        # log 20 messages

        for i in range(20):
            log.log(Debug("This is a debug message"))

        message = Debug("This is a special debug message")

        log.squash(message)

        self.assertEqual(len(log), 1)
        self.assertTrue(message in log)

    def test_LogNode_log_closure_message(self):
        """test the log_closure_message argument"""
        log = LogNode(name="Test", log_file="blagh6.log")

        # log 20 messages

        for i in range(20):
            log.log(Debug("This is a debug message"))

        del log

        with open("blagh6.log") as f:
            self.assertEqual(len(f.readlines()), 21)

    def test_logNode_no_log_when_closed(self):
        """test the log_when_closed argument"""
        log = LogNode(name="Test", log_file="blagh7.log", log_when_closed=False)

        # log 20 messages

        for i in range(20):
            log.log(Debug("This is a debug message"))

        del log

        with open("blagh7.log") as f:
            self.assertEqual(len(f.readlines()), 20)

    def test_logNode_repr_dunder(self):
        """test the __repr__ dunder"""
        log = LogNode(name="Test", log_file="blagh8.log", log_when_closed=False)
        self.assertEqual(repr(log), "LogNode Test at output blagh8.log")
        log = LogNode(name="Test", log_file="blagh8.log", log_when_closed=False, print_to_console=True)
        self.assertEqual(repr(log), "LogNode Test at output blagh8.log")
        log = LogNode(name="Test", log_when_closed=False, print_to_console=True)
        self.assertEqual(repr(log), "LogNode Test at output console")
        log = LogNode(name="Test", log_when_closed=False)
        self.assertEqual(repr(log), "LogNode Test at output None")

    def test_logNode_getitem_dunder(self):
        """test the __getitem__ dunder"""
        log = LogNode(name="Test", log_file="blagh9.log", log_when_closed=False)
        # log 20 messages
        specific_message = Debug("This is a debug message")
        for i in range(20):
            log.log(specific_message)
        self.assertEqual(log[0], specific_message)
        self.assertEqual(log[19], specific_message)
        self.assertRaises(IndexError, lambda: log[20])

        # assert two different objects with the same message are NOT equal
        self.assertFalse(log[0] == Debug("This is a debug message"))  # should be False

    def test_logNode_iter_dunder(self):
        """test the __iter__ dunder"""
        log = LogNode(name="Test", log_file="blagh10.log", log_when_closed=False)
        # log 20 messages
        specific_messages = [Debug("This is a debug message") for i in range(20)]
        for i in range(20):
            log.log(specific_messages[i])
        for index, i in enumerate(log):
            self.assertEqual(i, specific_messages[index])


class TestLogMessage(unittest.TestCase):
    """Test the LogMessage class"""

    def test_sub_LogMessage_creation(self):
        messages = gen_random_messages(50, extra_classes=[TestFilter.CustomMessage])

        for i in messages:
            self.assertTrue(isinstance(i, LogMessage))

    def test_sub_LogMessage_str(self):
        messages = gen_random_messages(50, extra_classes=[TestFilter.CustomMessage])

        for i in messages:
            try:
                str(i)
            except Exception as e:
                self.fail(e)

    def test_sub_LogMessage_colored(self):
        messages = gen_random_messages(50, extra_classes=[TestFilter.CustomMessage])

        for i in messages:
            try:
                i.colored()
            except Exception as e:
                self.fail(e)

    def test_sub_LogMessage_repr(self):

        messages = gen_random_messages(50, extra_classes=[TestFilter.CustomMessage])

        for i in messages:
            try:
                repr(i)
            except Exception as e:
                self.fail(e)

    def test_sub_LogMessage_eq(self):
        messages = gen_random_messages(50, extra_classes=[TestFilter.CustomMessage])

        for index, i in enumerate(messages):
            x = i
            y = messages[index + 1 if index + 1 < len(messages) else 0]
            self.assertTrue(i == x)
            self.assertFalse(i == y)

    def test_sub_LogMessage_ne(self):
        messages = gen_random_messages(50, extra_classes=[TestFilter.CustomMessage])

        for index, i in enumerate(messages):
            x = i
            y = messages[index + 1 if index + 1 < len(messages) else 0]
            self.assertFalse(i != x)
            self.assertTrue(i != y)


class TestCleanup(unittest.TestCase):
    """cleanup the chaos created by the tests"""

    def test_cleanup(self):
        # delete all the *.log.* files
        for i in os.listdir():
            if i.endswith(".log"):
                os.remove(i)
        self.assertTrue(True)
