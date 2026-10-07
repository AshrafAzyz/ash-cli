import platform

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
