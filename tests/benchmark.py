"""benchmarking for objlog"""
import objlog

log = objlog.LogNode("benchmark")


v = log.log(objlog.LogMessages.Info("benchmark test"), verbose=True)

print(v)

log.print = True

v = log.log(objlog.LogMessages.Info("benchmark test"), verbose=True)

print(v)
