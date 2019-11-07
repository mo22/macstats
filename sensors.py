import time
import psutil
from typing import List


class PsUtilSensor:
    def __init__(self):
        self.cpu_count_logical = psutil.cpu_count(True)
        self.cpu_count_physical = psutil.cpu_count(False)
        self.net = None
        self.disk = None
        self.time = None
        self.refresh()

    def refresh(self) -> None:
        self.time_last = self.time
        self.time = time.time()
        self.cpu_freq = psutil.cpu_freq(True)
        self.cpu_percent = psutil.cpu_percent(0, True)
        self.net_last = self.net
        self.net = psutil.net_io_counters(True)
        self.disk_last = self.disk
        self.disk = psutil.disk_io_counters(True)
        self.virtual_memory = psutil.virtual_memory()

        def fetch_process(process: psutil.Process):
            cpu_percent = None
            try:
                cpu_percent = process.cpu_percent
            except Exception:
                pass
            return (process, cpu_percent)
        self.processes = [fetch_process(process) for process in psutil.process_iter()]

    def get_cpu_percent_max(self) -> float:
        return max(self.cpu_percent)

    def get_cpu_percent_avg(self) -> float:
        return sum(self.cpu_percent) / len(self.cpu_percent)

    def get_disk_devs(self) -> List[str]:
        return self.disk.keys()

    def get_disk_write_bytes_per_sec(self, dev: str) -> float:
        if self.disk_last is None:
            return 0
        return (
            (self.disk[dev].write_bytes - self.disk_last[dev].write_bytes)
            / (self.time - self.time_last)
        )

    def get_disk_read_bytes_per_sec(self, dev: str) -> float:
        if self.disk_last is None:
            return 0
        return (
            (self.disk[dev].read_bytes - self.disk_last[dev].read_bytes)
            / (self.time - self.time_last)
        )

    def get_processes_by_cpu(self):
        res = sorted([
            (process, process.cpu_percent(None))
            for process in self.processes
        ], lambda i: i[1])
        return res


if __name__ == '__main__':
    sensor = PsUtilSensor()
    time.sleep(0.5)
    sensor.refresh()

    from pprint import pprint
    pprint(sensor.processes)
