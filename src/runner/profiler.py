import subprocess
from threading import Thread


class IProfiler:
    def begin(self, pid):
        pass

    def end(self) -> float:
        pass

    def unit(self) -> str:
        pass


class GpuMemDeltaProfiler(IProfiler, Thread):
    def __init__(self):
        super(GpuMemDeltaProfiler, self).__init__()
        self.stopped = False
        self.mem_offset = self.__mem()
        self.mem_max = 0

    @staticmethod
    def __mem():
        try:
            ps = subprocess.Popen('nvidia-smi', stdout=subprocess.PIPE)
            out = subprocess.check_output(('grep', 'redis'), stdin=ps.stdout)
            return int(out.decode().split()[-2][:-3])
        except subprocess.CalledProcessError:
            return 0

    def run(self):
        while not self.stopped:
            self.mem_max = max(self.mem_max, self.__mem())

    def begin(self, *_):
        super(GpuMemDeltaProfiler, self).start()

    def end(self):
        self.stopped = True
        self.join()
        return self.mem_max - self.mem_offset

    def unit(self) -> str:
        return "mb"
