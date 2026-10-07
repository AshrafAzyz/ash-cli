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

def show_status():
    info = get_memory_info()
    uptime = get_uptime()
    disk = get_disk_info()
    cpu = get_cpu_info()
    memory_usage, swap_usage = calculate_memory_usage(info)
    disk_usage = calculate_disk_usage(disk)

    #kB - MB - GB
    mem_total = info["MemTotal"]/1024/1024
    mem_free = info["MemFree"]/1024/1024
    mem_available = info["MemAvailable"]/1024/1024

    print("CPU:", cpu
    , "logical CPUs")
    print(f"Memory Total: {mem_total:.2f} GiB")
    print(f"Memory Free: {mem_free:.2f} GiB")
    print(f"Memory Available: {mem_available:.2f} GiB")
    print(f"Memory Usage: {memory_usage:.2f} %")
    print(f"Swap Usage: {swap_usage:.2f} %")
    print(f"Disk Usage: {disk_usage:.2f} %")
    print(f"Uptime: {uptime[0]} hours {uptime[1]} minutes {uptime[2]} seconds")
