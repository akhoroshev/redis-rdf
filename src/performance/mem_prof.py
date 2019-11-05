from memory_profiler import memory_usage
from multiprocessing.pool import ThreadPool


class MemDeltaProfiler:
    def __init__(self):
        self.pool = ThreadPool(1)
        self.start_mem = None
        self.async_result = None

    def start(self, pid, interval, timeout):
        self.start_mem = memory_usage(pid, max_usage=True, include_children=True)
        self.async_result = self.pool.apply_async(memory_usage, (pid, interval, timeout), {'max_usage': True})

    def end(self):
        return self.async_result.get() - self.start_mem
