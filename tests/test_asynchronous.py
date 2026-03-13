"""Asynchronous-only tests for ObjLog behavior."""

import os
import random
import time
import unittest

from objlog import LogMessage, LogNode
from objlog.LogMessages import Info

LOG_FOLDER = os.path.join(os.path.dirname(__file__), "logs")


class CustomMessage(LogMessage):
    color = "\033[0m"
    level = "CUSTOM"


def gen_random_messages(amount: int, extra_classes: list | None = None):
    messages = []
    extra_classes = extra_classes or []
    for _ in range(amount):
        cls = random.choice([Info] + extra_classes)
        messages.append(cls("This is a random message"))
    return messages


class TestAsyncLogNode(unittest.TestCase):
    def setUp(self):
        os.makedirs(LOG_FOLDER, exist_ok=True)
        for file_name in os.listdir(LOG_FOLDER):
            if file_name != ".gitkeep":
                os.remove(os.path.join(LOG_FOLDER, file_name))
        self.log = LogNode("Async", log_file=os.path.join(LOG_FOLDER, "AsyncTest.log"), asynchronous=True, log_when_closed=False)

    def tearDown(self):
        self.log.await_finish()
        self.log.wipe_messages(wipe_logfiles=True)
        self.log.await_finish()

    def test_async_queue_order_is_preserved(self):
        messages = gen_random_messages(100, extra_classes=[CustomMessage])
        for message in messages:
            self.log.log(message)
        self.assertListEqual(messages, self.log.get())

    def test_async_busy_reflects_pending_queue(self):
        def blocker(_bypass_async: bool = False):
            time.sleep(0.03)

        self.log.command_queue.put((blocker, (), {}))
        self.log.command_queue.put((blocker, (), {}))
        self.log.command_queue.put((blocker, (), {}))
        self.assertTrue(self.log.busy())
        self.log.await_finish()
        self.assertFalse(self.log.busy())

    def test_async_toggling_worker_thread_lifecycle(self):
        self.log.log(Info("before toggle"))
        self.log.await_finish()
        self.assertTrue(self.log.worker_thread.is_alive())

        self.log.asynchronous = False
        self.assertFalse(self.log.worker_thread.is_alive())
        self.log.log(Info("sync message"))
        self.assertEqual(2, len(self.log))

        self.log.asynchronous = True
        self.log.log(Info("after toggle"))
        self.log.await_finish()
        self.assertTrue(self.log.worker_thread.is_alive())
        self.assertEqual(3, len(self.log))

    def test_disable_enable_works_in_async_mode(self):
        self.log.disable()
        self.log.log(Info("should not log"))
        self.log.await_finish()
        self.assertEqual(0, len(self.log))

        self.log.enable()
        self.log.log(Info("should log"))
        self.log.await_finish()
        self.assertEqual(1, len(self.log))
