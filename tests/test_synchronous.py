"""Synchronous contract and edge-case tests for ObjLog."""

import datetime
import io
import os
import pickle
import random
import unittest
from contextlib import redirect_stdout

import objlog
from objlog import LogMessage, LogNode, utils
from objlog.LogMessages import Debug, Error, Fatal, Info, PythonExceptionMessage, Warn
from objlog.constants import VERSION_MAJOR

LOG_FOLDER = os.path.join(os.path.dirname(__file__), "logs")


class CustomMessage(LogMessage):
    color = "\033[0m"
    level = "CUSTOM"


def gen_random_messages(amount: int, extra_classes: list | None = None):
    messages = []
    extra_classes = extra_classes or []
    for _ in range(amount):
        cls = random.choice([Debug, Info, Warn, Error, Fatal] + extra_classes)
        messages.append(cls("This is a random message"))
    return messages


class TestLogNode(unittest.TestCase):
    def setUp(self):
        # make log folder and delete old logs
        os.makedirs(LOG_FOLDER, exist_ok=True)
        for file_name in os.listdir(LOG_FOLDER):
            if file_name != ".gitkeep":
                os.remove(os.path.join(LOG_FOLDER, file_name))

        # log nodes.
        self.log = LogNode("Test", log_file=os.path.join(LOG_FOLDER, "LogNodeTest.log"), log_when_closed=False)
        self.log2 = LogNode("Test2", log_file=os.path.join(LOG_FOLDER, "LogNodeTest2.log"), log_when_closed=False)
        self.log_at_console = LogNode("Console", print_to_console=True, log_when_closed=False)

    def tearDown(self):
        # clean everything up
        for node in (self.log, self.log2, self.log_at_console):
            node.wipe_messages(wipe_logfiles=True)
            node.enable()

    def test_log_basic_and_dunders(self):
        # test builtin python dunders on lognode
        msgs = [Debug("a"), Info("b"), Warn("c")]
        self.log.log(*msgs)
        self.assertEqual(3, len(self.log))
        self.assertListEqual(msgs, self.log.get())
        self.assertIs(msgs[0], self.log[0])
        self.assertIn(msgs[1], self.log)
        self.assertEqual(3, len(list(iter(self.log))))

    def test_wipe_messages_and_clear_log_paths(self):
        messages = gen_random_messages(20, extra_classes=[CustomMessage])
        self.log.log(*messages)
        self.log.wipe_messages()
        self.assertEqual(0, len(self.log))
        with open(self.log.log_file) as f:
            self.assertEqual(20, len(f.readlines()))

        self.log.log(*messages)
        self.log.clear_log()
        self.assertEqual(20, len(self.log))
        with open(self.log.log_file) as f:
            self.assertEqual(0, len(f.readlines()))

    def test_wipe_messages_and_logfiles(self):
        self.log.log(*gen_random_messages(15))
        self.log.wipe_messages(wipe_logfiles=True)
        self.assertEqual(0, len(self.log))
        with open(self.log.log_file) as f:
            self.assertEqual(0, len(f.readlines()))

    def test_star_log_equals_repeated(self):
        messages = gen_random_messages(10)
        self.log.log(*messages)
        log_star = self.log.get()
        self.log.wipe_messages(wipe_logfiles=True)
        for m in messages:
            self.log.log(m)
        self.assertListEqual(log_star, self.log.get())

    def test_log_type_validation(self):
        with self.assertRaises(TypeError):
            #noinspection PyTypeChecker
            self.log.log("not a LogMessage")

    def test_preserve_message_in_memory_false(self):
        self.log.log(Info("persist only to file"), preserve_message_in_memory=False)
        self.assertEqual(0, len(self.log))
        with open(self.log.log_file) as f:
            self.assertEqual(1, len(f.readlines()))

    def test_force_print_and_print_filter(self):
        filtered_log = LogNode("Filtered", print_to_console=True, print_filter=[Error], log_when_closed=False)
        try:
            out = io.StringIO()
            with redirect_stdout(out):
                filtered_log.log(Info("skip"), Error("print me"), force_print=(True, True))
            self.assertIn("print me", out.getvalue())
            self.assertNotIn("skip", out.getvalue())
        finally:
            filtered_log.wipe_messages()

    def test_filter_logfiles_true(self):
        self.log.log(Debug("debug"), Info("info"), CustomMessage("custom"))
        self.log.filter(CustomMessage, filter_logfiles=True)
        self.assertEqual(1, len(self.log))
        with open(self.log.log_file) as f:
            contents = f.read()
            self.assertIn("CUSTOM", contents)
            self.assertNotIn("DEBUG", contents)

    def test_filter_multiple_types(self):
        self.log.log(Debug("debug"), Info("info"), CustomMessage("custom"))
        self.log.filter(CustomMessage, Debug)
        filtered = self.log.get()
        self.assertEqual(2, len(filtered))
        self.assertTrue(all(isinstance(msg, (CustomMessage, Debug)) for msg in filtered))

    def test_dump_messages_variants(self):
        self.log.log(Debug("a"), CustomMessage("b"), Error("c"))
        dump_file = os.path.join(LOG_FOLDER, "dump.log")
        self.log.dump_messages(dump_file, CustomMessage)
        with open(dump_file) as f:
            lines = f.readlines()
        self.assertEqual(1, len(lines))
        self.assertIn("CUSTOM", lines[0])

        self.log.dump_messages(os.path.join(LOG_FOLDER, "wipe.log"), wipe_messages_from_memory=True)
        self.assertEqual(0, len(self.log))

    def test_dump_messages_filtered_multiple_types(self):
        self.log.log(Debug("a"), CustomMessage("b"), Error("c"), Info("d"))
        dump_file = os.path.join(LOG_FOLDER, "dump_multiple.log")
        self.log.dump_messages(dump_file, CustomMessage, Debug)
        with open(dump_file) as f:
            lines = f.readlines()
        self.assertEqual(2, len(lines))
        for line in lines:
            self.assertTrue("CUSTOM" in line or "DEBUG" in line)

    def test_dump_messages_to_console_filter(self):
        self.log.log(Debug("a"), Error("b"))
        out = io.StringIO()
        with redirect_stdout(out):
            self.log.dump_messages_to_console(Error)
        self.assertIn("ERROR", out.getvalue())
        self.assertNotIn("DEBUG", out.getvalue())

    def test_combine_merge_true_and_false(self):
        m1 = gen_random_messages(5)
        m2 = gen_random_messages(5)
        self.log.log(*m1)
        self.log2.log(*m2)

        self.log2.combine(self.log, merge_log_files=False)
        with open(self.log2.log_file) as f:
            file_line_count = len(f.readlines())
        self.assertEqual(5, file_line_count)
        self.assertEqual(10, len(self.log2))

        self.log2.combine(self.log, merge_log_files=True)
        with open(self.log2.log_file) as f:
            merged_line_count = len(f.readlines())
        self.assertEqual(len(self.log2), merged_line_count)

    def test_combine_order_preservation(self):
        left = [CustomMessage("left-1"), Debug("left-2")]
        right = [Info("right-1"), Warn("right-2")]
        self.log.log(*left)
        self.log2.log(*right)
        self.log2.combine(self.log)
        self.assertListEqual(right + left, self.log2.get())

    def test_squash_without_logfile_rewrite(self):
        self.log.log(*gen_random_messages(3))
        self.log.squash(Info("squashed"), squash_logfile=False)
        self.assertEqual(1, len(self.log))
        with open(self.log.log_file) as f:
            self.assertEqual(3, len(f.readlines()))

    def test_max_limits_and_truncation(self):
        log = LogNode("Cap", max_messages_in_memory=3, max_log_messages=3,
                      log_file=os.path.join(LOG_FOLDER, "cap.log"), log_when_closed=False)
        try:
            log.log(*gen_random_messages(6))
            self.assertEqual(3, len(log))
            with open(log.log_file) as f:
                self.assertEqual(3, len(f.readlines()))

            log.set_max_messages_in_memory(2)
            self.assertEqual(2, len(log))
            log.set_max_messages_in_log(2)
            with open(log.log_file) as f:
                self.assertEqual(2, len(f.readlines()))
        finally:
            log.wipe_messages(wipe_logfiles=True)

    def test_wipe_log_file_on_init_and_init_crop_existing_file(self):
        path = os.path.join(LOG_FOLDER, "init.log")
        with open(path, "w") as f:
            f.writelines([f"line-{i}\n" for i in range(10)])

        log = LogNode("Init", log_file=path, max_log_messages=4, log_when_closed=False)
        try:
            with open(path) as f:
                self.assertEqual(4, len(f.readlines()))
        finally:
            log.wipe_messages(wipe_logfiles=True)

        with open(path, "w") as f:
            f.writelines(["old\n"])
        log2 = LogNode("Init", log_file=path, wipe_log_file_on_init=True, log_when_closed=False)
        try:
            with open(path) as f:
                self.assertEqual(0, len(f.readlines()))
        finally:
            log2.wipe_messages(wipe_logfiles=True)

    def test_set_output_file_behaviors(self):
        first = os.path.join(LOG_FOLDER, "first.log")
        second = os.path.join(LOG_FOLDER, "second.log")
        log = LogNode("Switch", log_file=first, log_when_closed=False)
        try:
            log.log(Info("a"), Info("b"))

            # no-op when setting same file
            log.set_output_file(first)
            log.log(Info("c"))
            with open(first) as f:
                self.assertEqual(3, len(f.readlines()))

            log.set_output_file(second, preserve_old_messages=True)
            with open(second) as f:
                self.assertEqual(3, len(f.readlines()))

            log.set_output_file(None)
            log.log(Info("memory only"))
            self.assertEqual(4, len(log))
            with open(second) as f:
                self.assertEqual(3, len(f.readlines()))
        finally:
            log.wipe_messages(wipe_logfiles=True)

    def test_override_output_file(self):
        override = os.path.join(LOG_FOLDER, "override.log")
        self.log.log(Info("override"), override_log_file=override)
        with open(override) as f:
            self.assertEqual(1, len(f.readlines()))
        with open(self.log.log_file) as f:
            self.assertEqual(0, len(f.readlines()))

    def test_has_and_errors_and_exception_filtering(self):
        self.log.log(ImportError("bad import"), Warn("warn"), Error("err"))
        self.assertTrue(self.log.has(ImportError))
        self.assertTrue(self.log.has_errors())
        filtered = self.log.get(ImportError)
        self.assertEqual(1, len(filtered))
        self.assertIsInstance(filtered[0], PythonExceptionMessage)
        self.assertIsInstance(filtered[0].exception, ImportError)

    def test_get_filtered_python_exceptions_multiple_types(self):
        self.log.log(ImportError("bad import"), ZeroDivisionError("div by 0"), CustomMessage("custom"), Info("info"))
        filtered = self.log.get(ImportError, ZeroDivisionError, CustomMessage)
        self.assertEqual(3, len(filtered))
        self.assertTrue(any(isinstance(msg, CustomMessage) for msg in filtered))
        python_ex = [msg for msg in filtered if isinstance(msg, PythonExceptionMessage)]
        self.assertEqual(2, len(python_ex))

    def test_logging_default_python_exceptions_matrix(self):
        exceptions = [
            ImportError("import"),
            ZeroDivisionError("zero"),
            NotImplementedError("todo"),
            RecursionError("recur"),
            KeyboardInterrupt("kbd"),
            EOFError("eof"),
            StopIteration("stop"),
            GeneratorExit("gen"),
            SystemExit("sys exit"),
            SystemError("sys"),
            Warning("warn"),
        ]
        for exc in exceptions:
            self.log.log(exc)
        converted = self.log.get(PythonExceptionMessage)
        self.assertEqual(len(exceptions), len(converted))
        self.assertTrue(all(isinstance(msg.exception, BaseException) for msg in converted))

    def test_enabled_flag_constructor_and_toggle(self):
        log = LogNode("Disabled", enabled=False, log_when_closed=False)
        try:
            log.log(Info("nope"))
            self.assertEqual(0, len(log))
            log.enable()
            log.log(Info("yep"))
            self.assertEqual(1, len(log))
            log.disable()
            log.log(Info("nope again"))
            self.assertEqual(1, len(log))
        finally:
            log.wipe_messages(wipe_logfiles=True)

    def test_rename_and_update_logs(self):
        self.log.log(*gen_random_messages(8))
        with open(self.log.log_file) as f:
            before_lines = f.readlines()
        self.assertGreater(len(before_lines), 0)

        self.log.rename("Renamed", update_in_logs=True)
        with open(self.log.log_file) as f:
            after_lines = f.readlines()

        self.assertEqual(len(before_lines), len(after_lines))
        self.assertTrue(all("[Renamed]" in line for line in after_lines))

    def test_save_and_load_and_load_failures(self):
        base = os.path.join(LOG_FOLDER, "node")
        self.log.log(Info("persist"))
        self.log.save(base)
        loaded = objlog.load(base + ".lgnd")
        self.assertEqual(self.log.uuid, loaded.uuid)

        bad_type = os.path.join(LOG_FOLDER, "bad_type.lgnd")
        with open(bad_type, "wb") as f:
            pickle.dump({"not": "lognode"}, f)
        with self.assertRaises(TypeError):
            objlog.load(bad_type)

        bad_version = os.path.join(LOG_FOLDER, "bad_version.lgnd")
        stale = LogNode("stale", log_when_closed=False)
        stale.version = VERSION_MAJOR + 99
        with open(bad_version, "wb") as f:
            pickle.dump(stale, f)
        with self.assertRaises(ValueError):
            objlog.load(bad_version)

    def test_verbose_output_shape(self):
        messages = gen_random_messages(4, extra_classes=[CustomMessage])
        result = self.log.log(*messages, verbose=True)
        self.assertIn("processtime_ns", result)
        self.assertIn("logged", result)
        self.assertEqual(4, len(result["logged"]))
        self.assertTrue(all("message" in i and "id_in_node" in i and "type" in i for i in result["logged"]))

    def test_monitor_decorator_behaviors(self):
        @utils.monitor(self.log)
        def swallow():
            raise RuntimeError("boom")

        swallow()
        self.assertTrue(self.log.has_errors())

        @utils.monitor(self.log, raise_exceptions=True)
        def raise_it():
            raise RuntimeError("boom2")

        with self.assertRaises(RuntimeError):
            raise_it()

        @utils.monitor(self.log, exit_on_exception=True, raise_exceptions=True)
        def exit_wins():
            raise RuntimeError("boom3")

        with self.assertRaises(SystemExit):
            exit_wins()

        @utils.monitor(self.log)
        def returns():
            return 42

        self.assertEqual(42, returns())

    def test_logfile_deletion_mid_run(self):
        for i in range(50):
            self.log.log(Info(f"msg-{i}"))
            if i == 20 and os.path.exists(self.log.log_file):
                os.remove(self.log.log_file)
        self.assertTrue(os.path.exists(self.log.log_file))
        with open(self.log.log_file) as f:
            self.assertGreater(len(f.readlines()), 0)


class TestLogMessage(unittest.TestCase):
    def test_logmessage_hates_being_used_directly(self):
        with self.assertRaises(TypeError):
            LogMessage("direct")

    def test_builtin_and_custom_are_logmessages(self):
        self.assertIsInstance(Debug("x"), LogMessage)
        self.assertIsInstance(Info("x"), LogMessage)
        self.assertIsInstance(Warn("x"), LogMessage)
        self.assertIsInstance(Error("x"), LogMessage)
        self.assertIsInstance(Fatal("x"), LogMessage)
        self.assertIsInstance(CustomMessage("x"), LogMessage)
        self.assertIsInstance(PythonExceptionMessage(Exception("x")), LogMessage)

    def test_colored_and_string_representations(self):
        message = CustomMessage("hello")
        dt = datetime.datetime.fromtimestamp(message.unix / 1000).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        self.assertEqual(f"[{dt}] CUSTOM: hello", str(message))
        self.assertEqual("CUSTOM: hello", repr(message))
        self.assertTrue(message.colored().startswith("\033[0m["))

    def test_logmessage_identity(self):
        self.assertNotEqual(Debug("x"), Debug("x"))
        msg = CustomMessage("same")
        self.assertEqual(msg, msg)
