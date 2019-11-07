import time
import psutil


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
        self.processes = list(psutil.process_iter())
        for process in self.processes:
            try:
                process.cpu_percent(None)
            except psutil.NoSuchProcess:
                pass
            except psutil.AccessDenied:
                pass

    def get_cpu_percent_max(self):
        return max(self.cpu_percent)

    def get_cpu_percent_avg(self):
        return sum(self.cpu_percent) / len(self.cpu_percent)

    def get_disk_devs(self):
        return self.disk.keys()

    def get_disk_write_bytes_per_sec(self, dev):
        if self.disk_last is None:
            return 0
        return (
            (self.disk[dev].write_bytes - self.disk_last[dev].write_bytes)
            / (self.time - self.time_last)
        )

    def get_disk_read_bytes_per_sec(self, dev):
        if self.disk_last is None:
            return 0
        return (
            (self.disk[dev].read_bytes - self.disk_last[dev].read_bytes)
            / (self.time - self.time_last)
        )
