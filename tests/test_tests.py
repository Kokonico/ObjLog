"""test the functionality of the logger"""

import unittest
import random

from objlog import LogNode, LogMessage
from objlog.LogMessages import Debug, Info, Warn, Error, Fatal

# delete all .logs

import os

for i in os.listdir():
    if i.endswith(".log"):
        os.remove(i)


def gen_random_messages(amount: int, extra_classes: list = []):
    """generate random messages"""
    messages = []
    for i in range(amount):
        messages.append(random.choice([Debug, Info, Warn, Error, Fatal] + extra_classes)("This is a random message"))
    return messages


class TestFilter(unittest.TestCase):
    """test the filtering functionality of the logger"""

    # new log node

    log = LogNode(name="Test", log_file="test.log")

    class custom_message(LogMessage):
        level = "CUSTOM"
        color = "\033[1;35m"  # purple

    def test_live_filter(self):

        # log 20 messages, all of them random

        for i in gen_random_messages(20, extra_classes=[self.custom_message]):
            self.log.log(i)

        self.log.filter([Debug])

        # use for loop to test the filter

        for message in self.log.get(element_filter=[Debug, Info, Warn, Error, Fatal,
                                                    self.custom_message]):  # get all the messages (to avoid double-dipping)
            self.assertEqual(message.level, "DEBUG")

    def test_get_filter(self):
        """test the get() function's filter argument"""
        for i in gen_random_messages(20, extra_classes=[self.custom_message]):
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

        for message in self.log.get(element_filter=[self.custom_message]):
            self.assertEqual(message.level, "CUSTOM")

    def test_filter_logfiles(self):
        """test the filter_logfiles argument"""
        for i in gen_random_messages(20, extra_classes=[self.custom_message]):
            self.log.log(i)
        self.log.filter([Debug], filter_logfiles=True)
        with open("test.log") as f:
            for line in f.readlines():
                self.assertEqual(line.split(" ")[2], "DEBUG:")


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
        self.assertListEqual(log.get(element_filter=
                                     [Debug, Info, Warn, Error, Fatal]), [debug, info, warn, error, fatal]
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

        log.dump_messages("dump2.log", elementfilter=[Debug, Info, Warn, Error, Fatal], wipe_messages_from_memory=False)

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


class TestLogMessage(unittest.TestCase):
    """Test the LogMessage class"""

    def test_sub_LogMessage_creation(self):
        messages = gen_random_messages(50, extra_classes=[TestFilter.custom_message])

        for i in messages:
            self.assertTrue(isinstance(i, LogMessage))

    def test_sub_LogMessage_str(self):
        messages = gen_random_messages(50, extra_classes=[TestFilter.custom_message])

        for i in messages:
            try:
                str(i)
            except Exception as e:
                self.fail(e)

    def test_sub_LogMessage_colored(self):
        messages = gen_random_messages(50, extra_classes=[TestFilter.custom_message])

        for i in messages:
            try:
                i.colored()
            except Exception as e:
                self.fail(e)

    def test_sub_LogMessage_repr(self):

        messages = gen_random_messages(50, extra_classes=[TestFilter.custom_message])

        for i in messages:
            try:
                repr(i)
            except Exception as e:
                self.fail(e)

    def test_sub_LogMessage_eq(self):
        messages = gen_random_messages(50, extra_classes=[TestFilter.custom_message])

        for index, i in enumerate(messages):
            x = i
            y = messages[index + 1 if index + 1 < len(messages) else 0]
            self.assertTrue(i == x)
            self.assertFalse(i == y)

    def test_sub_LogMessage_ne(self):
        messages = gen_random_messages(50, extra_classes=[TestFilter.custom_message])

        for index, i in enumerate(messages):
            x = i
            y = messages[index + 1 if index + 1 < len(messages) else 0]
            self.assertFalse(i != x)
            self.assertTrue(i != y)
