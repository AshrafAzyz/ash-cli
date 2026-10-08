import platform
import json

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

def get_system_info():
    info = get_os_release()
    kernel = platform.release()
    arch = platform.machine()
    python = platform.python_version()
    hostname = platform.node()

    return {
        "os": info["NAME"],
        "version": info["VERSION_ID"],
        "codename": info.get("VERSION_CODENAME"),
        "kernel": kernel,
        "architecture": arch,
        "python": python,
        "hostname": hostname
    }

def show_system(json_output):
    data = get_system_info()

    if json_output:
        print(json.dumps(data, indent=4))
        return

    print("OS:", data["os"])
    print("Version:", data["version"])
    print("Codename:", data["codename"])
    print("Kernel:", data["kernel"])
    print("Architecture:", data["architecture"])
    print("Python:", data["python"])
    print("Hostname:", data["hostname"])
