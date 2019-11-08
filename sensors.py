import time
import psutil
from typing import List, NamedTuple, Optional


class PsUtilProcess(NamedTuple):
    process: psutil.Process
    name: str
    cpu_percent: Optional[float]


class PsUtilSensor:
    cpu_count_logical: int
    cpu_count_physical: int

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
            name = None
            try:
                cpu_percent = process.cpu_percent()
                name = process.name()
            except Exception:
                pass
            return PsUtilProcess(
                process=process,
                name=name,
                cpu_percent=cpu_percent,
            )
        self.processes = [fetch_process(process) for process in psutil.process_iter()]

    def get_cpu_percent_max(self) -> float:
        return max(self.cpu_percent)

    def get_cpu_percent_avg(self) -> float:
        return sum(self.cpu_percent) / len(self.cpu_percent)

    def get_cpu_percent_top(self) -> float:
        return self.get_processes_by_cpu()[0].cpu_percent

    def get_disk_devs(self) -> List[str]:
        return self.disk.keys()

    def get_disk_dev_most_active(self) -> Optional[str]:
        max_total = 0
        max_dev = None
        for dev in self.disk.keys():
            total = (
                self.get_disk_write_bytes_per_sec(dev)
                + self.get_disk_read_bytes_per_sec(dev)
            )
            if total > max_total:
                max_total = total
                max_dev = dev
        return max_dev

    def get_disk_write_bytes_per_sec(self, dev: str) -> float:
        if self.disk_last is None or dev not in self.disk_last:
            return 0
        return (
            (self.disk[dev].write_bytes - self.disk_last[dev].write_bytes)
            / (self.time - self.time_last)
        )

    def get_disk_read_bytes_per_sec(self, dev: str) -> float:
        if self.disk_last is None or dev not in self.disk_last:
            return 0
        return (
            (self.disk[dev].read_bytes - self.disk_last[dev].read_bytes)
            / (self.time - self.time_last)
        )

    def get_net_devs(self) -> List[str]:
        return self.net.keys()

    def get_net_dev_most_active(self) -> Optional[str]:
        max_total = 0
        max_dev = None
        for dev in self.net.keys():
            if dev.startswith('lo'):
                continue
            total = (
                self.get_net_recv_bytes_per_sec(dev)
                + self.get_net_sent_bytes_per_sec(dev)
            )
            if total > max_total:
                max_total = total
                max_dev = dev
        return max_dev

    def get_net_recv_bytes_per_sec(self, dev: str) -> float:
        if self.net_last is None or dev not in self.net_last:
            return 0
        return (
            (self.net[dev].bytes_recv - self.net_last[dev].bytes_recv)
            / (self.time - self.time_last)
        )

    def get_net_sent_bytes_per_sec(self, dev: str) -> float:
        if self.net_last is None or dev not in self.net_last:
            return 0
        return (
            (self.net[dev].bytes_sent - self.net_last[dev].bytes_sent)
            / (self.time - self.time_last)
        )

    def get_processes_by_cpu(self):
        return sorted(
            [i for i in self.processes if i.cpu_percent is not None],
            key=lambda i: -i.cpu_percent
        )


if __name__ == '__main__':
    sensor = PsUtilSensor()
    time.sleep(0.5)
    sensor.refresh()

    # from pprint import pprint
    # pprint(sensor.get_processes_by_cpu()[0:10])
    print(sensor.get_net_dev_most_active())
    print(sensor.get_disk_dev_most_active())
