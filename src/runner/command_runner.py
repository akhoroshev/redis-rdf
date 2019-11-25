from typing import Tuple, List, Any, Callable
from time import sleep

from redis import Redis

from .profiler import IProfiler


def run_command(redis_instance: Redis,
                redis_command: Tuple[str, ...],
                redis_pid: int,
                mem_profiler_factory: Callable[[], IProfiler]) -> List[Any]:
    cmd = lambda: [s.decode('UTF-8') if isinstance(s, bytes) else s for s in
                   redis_instance.execute_command(*redis_command)]
    if mem_profiler_factory:
        profiler = mem_profiler_factory()
        sleep(1)
        profiler.begin(redis_pid)
        cmd_result = cmd()
        mem_usage = profiler.end()
        cmd_result.insert(0, f'mem {profiler.unit()}: {mem_usage}')
    else:
        cmd_result = cmd()
    return cmd_result
