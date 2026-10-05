import argparse
import platform
import os
import shutil
import datetime
import status

parser = argparse.ArgumentParser(description = "A Linux system information CLI.")

subparsers = parser.add_subparsers(dest="command")

subparsers.add_parser(
	"status",
	help="Show system health information",
	description="Display CPU, memory, disk, uptime, and general system health."
)

subparsers.add_parser(
	"system",
	help="Show system information"
)

subparsers.add_parser(
	"services",
	help="Show systemd services"
)

def get_os_release():
    #get info
    with open('/etc/os-release') as file:
        data = file.read()

    info = {}

    for line in data.splitlines():
        key, value = line.split("=", 1)
        value = value.strip('"')
        info[key] = value

    return info

def show_status():
    info = status.get_memory_info()
    uptime = status.get_uptime()
    disk = status.get_disk_info()
    cpu = status.get_cpu_info()
    memory_usage, swap_usage = status.calculate_memory_usage(info)
    disk_usage = status.calculate_disk_usage(disk)

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

def show_system():
    info = get_os_release()
    kernel = platform.release()
    arch = platform.machine()
    python = platform.python_version()
    hostname = platform.node()

    print("OS:", info["NAME"])
    print("Version:", info["VERSION_ID"])
    print("Codename:", info["VERSION_CODENAME"])
    print("Kernel:", kernel)
    print("Architecture:", arch)
    print("Python:", python)
    print("Hostname:", hostname)

def show_services():
	print("Showing system services....")

args = parser.parse_args()

if args.command == "status":
	show_status()
elif args.command == "system":
	show_system()
elif args.command == "services":
	show_services()
