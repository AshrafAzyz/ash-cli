import datetime
import shutil
import os

def get_memory_info():
    with open('/proc/meminfo') as file:
        data = file.read()

    info = {}

    for line in data.splitlines():
        key, value = line.split(":", 1)
        value = int(value.strip(" kB"))
        info[key] = value

    return info

def get_uptime():
    with open('/proc/uptime') as file:
        data = file.read()

    uptime = str(datetime.timedelta(seconds=int(float(data.split(" ")[0])))).split(":", 3)

    return uptime

def get_disk_info():
    disk = shutil.disk_usage('/')
    return disk

def get_cpu_info():
    return os.cpu_count()

def calculate_memory_usage(info):
    #memory usage
    memory_usage = ((info["MemTotal"] - info["MemAvailable"])/info["MemTotal"])*100
    #swap usage
    swap_usage = ((info["SwapTotal"] - info["SwapFree"])/info["SwapTotal"])*100
    return memory_usage, swap_usage

def calculate_disk_usage(disk):
    #disk usage
    disk_usage = (disk.used/disk.total)*100
    return disk_usage
