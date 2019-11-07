import time
import psutil


if __name__ == '__main__':
    time.sleep(1)

    cpu = psutil.cpu_percent(0, True)
    cpu_max = max(cpu)
    cpu_avg = sum(cpu) / len(cpu)
    print('cpu_max', cpu_max)
    print('cpu_avg', cpu_avg)


# get cpu usage

# get cpu usage per process

# memory?

# check if high disk io?
# -> which process?

# check if high network io?
# -> which process?
