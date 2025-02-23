"""benchmarking for objlog"""
import os

import objlog

log = objlog.LogNode("benchmark")


v = log.log(objlog.LogMessages.Info("benchmark test"), verbose=True)

print(v)

log.print = True

v = log.log(objlog.LogMessages.Info("benchmark test"), verbose=True)

print(v)

log.set_output_file("benchmark.log")

v = log.log(objlog.LogMessages.Info("benchmark test"), verbose=True)
print(v)

log.print = False

v = log.log(objlog.LogMessages.Info("benchmark test"), verbose=True)

print(v)

os.remove("benchmark.log")
