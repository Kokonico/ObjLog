"""benchmarking for objlog"""
import os

import objlog

log = objlog.LogNode("benchmark", asynchronous=False)


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

os.remove("benchmark.log") if os.path.exists("benchmark.log") else None
# log.set_output_file(None)
# log.print = True

# test messages in 1 second
import time
start_time = time.time()
count = 0


while time.time() - start_time < 1:
    log.log(objlog.LogMessages.Debug("benchmark test"), verbose=False)
    count += 1

time_pre_finish = time.time()

log.await_finish()

print(f"Logged {count} messages in 1 second.")
print(f"Total time including await_finish: {time.time() - start_time} seconds.")
print(f"Time taken to await finish: {time.time() - time_pre_finish} seconds.")
print(f"Throughput: {count / (time.time() - start_time):.2f} messages/second.")
