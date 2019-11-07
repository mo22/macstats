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
        self.disk = psutil.net_io_counters(True)

        processes = list(psutil.process_iter())
        for process in processes:
            try:
                process.cpu_percent(None)
            except psutil.NoSuchProcess:
                pass
            except psutil.AccessDenied:
                pass
