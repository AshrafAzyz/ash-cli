import datetime
import shutil
import os
import json
import time
import subprocess

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

def get_network_info():
    try:
        result = subprocess.run(
            ["ip", "-brief", "addr"],
            capture_output=True,
            text=True
        )
    except FileNotFoundError:
        return []

    if result.returncode != 0:
        return []

    interfaces = []

    for line in result.stdout.splitlines():
        parts = line.split()

        if len(parts) < 3:
            continue

        interface = parts[0]
        state = parts[1]
        addresses = parts[2:]

        if interface == "lo":
            continue

        ipv4 = None
        ipv6 = None

        for address in addresses:
            if "/" not in address:
                continue

            if ":" in address:
                if ipv6 is None:
                    ipv6 = address
            else:
                if ipv4 is None:
                    ipv4 = address

        interfaces.append({
            "interface": interface,
            "state": state,
            "ipv4": ipv4,
            "ipv6": ipv6
        })

    return interfaces

def get_cpu_times():
    with open('/proc/stat') as file:
        line = file.readline()

    parts = line.split()

    user = int(parts[1])
    nice = int(parts[2])
    system = int(parts[3])
    idle = int(parts[4])

    return user, nice, system, idle

def get_cpu_usage():
    before = get_cpu_times()
    time.sleep(1)
    after = get_cpu_times()
    return calculate_cpu_usage(before,after)

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

def calculate_cpu_usage(before,after):
    before_total = sum(before)
    after_total = sum(after)

    total_delta = after_total - before_total
    idle_delta = after[3] - before[3]

    if total_delta ==0:
        return 0.0

    usage = ((total_delta - idle_delta) / total_delta) * 100

    return usage

def calculate_health(cpu_usage, memory_usage, disk_usage):
    if cpu_usage >= 90 or memory_usage >= 90 or disk_usage >= 90:
        return "CRITICAL"

    if cpu_usage >= 70 or memory_usage >= 70 or disk_usage >= 70:
        return "WARNING"

    return "OK"

def get_status_info():
    info = get_memory_info()
    uptime = get_uptime()
    disk = get_disk_info()
    cpu = get_cpu_info()
    cpu_usage = get_cpu_usage()
    load_average = get_load_average()
    network = get_network_info()

    memory_usage, swap_usage = calculate_memory_usage(info)
    disk_usage = calculate_disk_usage(disk)
    health = calculate_health(cpu_usage, memory_usage, disk_usage)

    return{
        "info": {
            "MemTotal":info["MemTotal"],
            "MemFree":info["MemFree"],
            "MemAvailable":info["MemAvailable"]
        },
        "uptime": uptime,
        "disk":disk,
        "cpu": cpu,
        "cpu_usage": cpu_usage,
        "load_average": load_average,
        "network": network,
        "memory_usage":memory_usage,
        "swap_usage": swap_usage,
        "disk_usage": disk_usage,
        "health": health
    }

def get_load_average():
    with open('/proc/loadavg') as file:
        data = file.read()

    parts = data.split()

    return {
        "1_minute": float(parts[0]),
        "5_minutes": float(parts[1]),
        "15_minutes": float(parts[2])
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

    print(f"Health: {data['health']}")
    print("---")

    print(f"CPU: {data['cpu']} logical CPUs")
    print(f"CPU Usage: {data['cpu_usage']:.2f} %")
    print(
        f"Load Average: "
        f"{data['load_average']['1_minute']:.2f}, "
        f"{data['load_average']['5_minutes']:.2f}, "
        f"{data['load_average']['15_minutes']:.2f}"
    )

    print("---")

    print(f"Memory Total: {mem_total:.2f} GiB")
    print(f"Memory Free: {mem_free:.2f} GiB")
    print(f"Memory Available: {mem_available:.2f} GiB")
    print(f"Memory Usage: {data['memory_usage']:.2f} %")

    print("---")

    print(f"Swap Usage: {data['swap_usage']:.2f} %")
    print(f"Disk Usage: {data['disk_usage']:.2f} %")

    print("---")

    for network in data["network"]:
        print(
            f"Network: {network['interface']} "
            f"({network['state']})"
        )

        print(f"IPv4: {network['ipv4']}")
        print(f"IPv6: {network['ipv6']}")

    print("---")

    print(
        f"Uptime: "
        f"{data['uptime']['days']} days "
        f"{data['uptime']['hours']} hours "
        f"{data['uptime']['minutes']} minutes "
        f"{data['uptime']['seconds']} seconds"
    )
