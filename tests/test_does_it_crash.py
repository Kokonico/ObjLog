"""The most basic test possible. Does it crash?"""

try:
    from objlog import LogNode, LogMessage
    from objlog.LogMessages import Debug, Info, Warn, Error, Fatal

    # create log node

    log = LogNode(name="Basic Example", print_to_console=True, max_log_messages=10, max_messages_in_memory=5,

                  log_when_closed=False, print_filter=[Debug, Info, Warn, Error, Fatal], log_file="log.log"
                  )  # all the parameters, just for testing.

    # log some messages

    log.log(Debug("This is a debug message"))
    log.log(Info("This is an info message"))
    log.log(Warn("This is a warning message"))
    log.log(Error("This is an error message"))
    log.log(Fatal("This is a fatal message"))

    # do some stuff

    log.set_max_messages_in_memory(10)
    log.set_max_messages_in_log(20)
    log.set_output_file("log.log", preserve_old_messages=True)
    log.dump_messages_to_console(elementfilter=[Debug, Info, Warn, Error, Fatal])
    log.dump_messages("dump.log", elementfilter=[Debug, Info, Warn, Error, Fatal], wipe_messages_from_memory=True)
    log.log(Debug("This is a debug message"))
    log.log(Info("This is an info message"))
    log.log(Warn("This is a warning message"))
    log.log(Error("This is an error message"))
    log.log(Fatal("This is a fatal message"))
    log.log(Debug("This is a debug message"))
    log.log(Info("This is an info message"))

    log.filter([Debug, Info], filter_logfiles=True)


    class CustomMessage(LogMessage):
        level = "CUSTOM"
        color = "\033[1;35m"  # purple


    log.log(CustomMessage("This is a custom message"))

    log.get(Debug, Info, Warn, Error, Fatal)

    len(log)

    print(log)

    del log
except Exception as e:
    print(f"Test failed: {e}")
    raise e
