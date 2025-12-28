"""async logging example using objlog"""
import sys

from objlog import LogNode
from objlog.LogMessages import Debug, Info

# create a log node that prints to console and logs to a file
log = LogNode(name="Async Logging Example", print_to_console=True)

# let's see how many messages we can log synchronously (in 1 second)
import time
sync_start_time = time.time()
sync_count = 0
while time.time() - sync_start_time < 1:
	log.log(Debug("synchronous debug message"))
	sync_count += 1

# now let's enable async logging
log.wipe_messages()

log.asynchronous = True  # Note: you can set this property at any time to switch between sync and async logging, the background thread will be started/stopped automatically

# let's see how many messages we can log asynchronously (in 1 second)
async_start_time = time.time()
async_count = 0
while time.time() - async_start_time < 1:
	log.log(Debug("asynchronous debug message"))
	async_count += 1
wait_queue_start_time = time.time()

log.await_finish()

log.log(Info(f"logged {sync_count} synchronous messages in 1 second"))
log.log(Info(f"queued {async_count} asynchronous messages in 1 second"))
log.log(Info(f"took {time.time() - wait_queue_start_time:.2f} seconds to write all asynchronous messages to disk post-queue"))
log.log(Info(('synchronous' if sync_count > async_count else 'asynchronous' if async_count > sync_count else 'both') + f' was the faster mode with a difference of {abs(async_count - sync_count)} messages more logged in 1 second (percentage difference: {abs(async_count - sync_count) / max(sync_count, async_count) * 100:.2f}% faster)' if sync_count != async_count else f' modes logged the same number of messages in 1 second ({sync_count} messages)'))

log.await_finish() # AWAIT FINISH AGAIN TO ENSURE ALL MESSAGES ARE WRITTEN BEFORE EXITING THE PROGRAM!!!
# OBJLOG DOES NOT GUARANTEE ALL MESSAGES ARE PROPERLY HANDLED UNTIL AWAIT_FINISH IS CALLED!!!

# now, it'll take quite a bit of time for the background thread to print all the queued message.
# it's way faster to queue the messages than to write them to disk, so we logged way more messages in async mode.
# On an intel i9-11900KF, it takes ~2 seconds to catch up
# logging to a file will significantly slow down the logging speed, so if you want to maximize logging speed, consider disabling file logging or logging to a faster medium (e.g., an in-memory filesystem or a ramdisk)
