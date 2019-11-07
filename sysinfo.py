import time
import psutil


if __name__ == '__main__':
    processes = list(psutil.process_iter())
    for process in processes:
        try:
            process.cpu_percent(None)
        except psutil.AccessDenied:
            pass

    time.sleep(0.5)

    print('psutil.cpu_freq', psutil.cpu_freq(True))

    print('psutil.cpu_count', psutil.cpu_count(False), psutil.cpu_count(True))

    print('psutil.cpu_times_percent', psutil.cpu_times_percent(0, True))

    cpu = psutil.cpu_percent(0, True)
    print('psutil.cpu_percent', cpu)
    cpu_max = max(cpu)
    cpu_avg = sum(cpu) / len(cpu)
    print(f"cpu max {cpu_max:.0f}% | avg {cpu_avg:.0f}%")
    # which process?

    # memory?
    print('psutil.virtual_memory', psutil.virtual_memory())

    # check if high disk io?
    # -> which process?
    print('psutil.disk_io_counters', psutil.disk_io_counters(True))

    # check if high network io?
    # -> which process?
    print('psutil.net_io_counters', psutil.net_io_counters(True))

    for process in processes:
        try:
            cpu_percent = process.cpu_percent(None)
            if cpu_percent > 0:
                print('process.cpu_percent', cpu_percent, process.pid, process.name())
        except psutil.AccessDenied:
            pass

    # for process in processes:
    #     try:
    #         print('process.memory_info', process.memory_info())
    #     except psutil.AccessDenied:
    #         pass
