import datetime
import shutil
import os
import json

def get_memory_info():
    with open('/proc/meminfo') as file:
        data = file.read()

    info = {}

    for line in data.splitlines():
        key, value = line.split(":", 1)
        value = int(value.removesuffix(" kB"))
        info[key] = value

    return info

def get_uptime():
    with open('/proc/uptime') as file:
        data = file.read()

    seconds = int(float(data.split(" ")[0]))
    uptime = datetime.timedelta(seconds=seconds)

    return {
        "days": uptime.days,
        "hours": uptime.seconds//3600,
        "minutes": (uptime.seconds % 3600) // 60,
        "seconds": uptime.seconds % 60
    }

def get_disk_info():
    disk = shutil.disk_usage('/')
    return {
        "total": disk.total,
        "used": disk.used,
        "free": disk.free,
    }

def get_cpu_info():
    return os.cpu_count()

def calculate_memory_usage(info):
    #memory usage
    memory_usage = ((info["MemTotal"] - info["MemAvailable"])/info["MemTotal"])*100

    #swap usage
    if info["SwapTotal"] == 0:
        swap_usage = 0.0
    else:
        swap_usage = ((info["SwapTotal"] - info["SwapFree"])/info["SwapTotal"])*100

    return memory_usage, swap_usage

def calculate_disk_usage(disk):
    #disk usage
    disk_usage = (disk["used"]/disk["total"])*100
    return disk_usage

def get_status_info():
    info = get_memory_info()
    uptime = get_uptime()
    disk = get_disk_info()
    cpu = get_cpu_info()
    memory_usage, swap_usage = calculate_memory_usage(info)
    disk_usage = calculate_disk_usage(disk)

    return{
        "info": {
            "MemTotal":info["MemTotal"],
            "MemFree":info["MemFree"],
            "MemAvailable":info["MemAvailable"]
        },
        "uptime": uptime,
        "disk":disk,
        "cpu": cpu,
        "memory_usage":memory_usage,
        "swap_usage": swap_usage,
        "disk_usage": disk_usage
    }

def show_status(json_status_output):
    data = get_status_info()

    #kB - MB - GB
    mem_total = data["info"]["MemTotal"]/1024/1024
    mem_free = data["info"]["MemFree"]/1024/1024
    mem_available = data["info"]["MemAvailable"]/1024/1024

    if json_status_output:
        print(json.dumps(data, indent=4))
        return

    print("CPU:", data["cpu"], "logical CPUs")
    print(f"Memory Total: {mem_total:.2f} GiB")
    print(f"Memory Free: {mem_free:.2f} GiB")
    print(f"Memory Available: {mem_available:.2f} GiB")
    print(f"Memory Usage: {data["memory_usage"]:.2f} %")
    print(f"Swap Usage: {data["swap_usage"]:.2f} %")
    print(f"Disk Usage: {data["disk_usage"]:.2f} %")
    print(f"Uptime: {data["uptime"]["days"]} days {data["uptime"]["hours"]} hours {data["uptime"]["minutes"]} minutes {data["uptime"]["seconds"]} seconds")
