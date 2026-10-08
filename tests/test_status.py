from unittest.mock import mock_open, patch
from types import SimpleNamespace
from ash import status

def test_calculate_health_ok():
    result = status.calculate_health(cpu_usage=40, memory_usage=50, disk_usage=60)
    assert result == "OK"

def test_calculate_health_warning():
    result = status.calculate_health(cpu_usage=70, memory_usage=50, disk_usage=60)
    assert result == "WARNING"

def test_get_memory_info():
    fake_meminfo = """MemTotal:       8000000 kB
MemFree:        2000000 kB
MemAvailable:   5000000 kB
SwapTotal:     4000000 kB
SwapFree:      3000000 kB
"""

    with patch(
        "builtins.open",
        mock_open(read_data=fake_meminfo)
    ):
        result = status.get_memory_info()

    assert result["MemTotal"] == 8000000
    assert result["MemFree"] == 2000000
    assert result["MemAvailable"] == 5000000
    assert result["SwapTotal"] == 4000000
    assert result["SwapFree"] == 3000000

def test_get_uptime():
    fake_uptime = "90061.5 12345.6\n"

    with patch(
        "builtins.open",
        mock_open(read_data=fake_uptime)
    ):
        result = status.get_uptime()

    assert result["days"] == 1
    assert result["hours"] == 1
    assert result["minutes"] == 1
    assert result["seconds"] == 1

def test_get_load_average():
    fake_loadavg = "1.25 0.75 0.50 2/345 12345\n"

    with patch(
        "builtins.open",
        mock_open(read_data=fake_loadavg)
    ):
        result = status.get_load_average()

    assert result["1_minute"] == 1.25
    assert result["5_minutes"] == 0.75
    assert result["15_minutes"] == 0.50

def test_get_network_info():
    fake_output = """lo               UNKNOWN        127.0.0.1/8 ::1/128
enp0s3           UP             192.168.1.10/24 fe80::1234/64
"""

    fake_result = SimpleNamespace(
        returncode=0,
        stdout=fake_output,
        stderr=""
    )

    with patch(
        "ash.status.subprocess.run",
        return_value=fake_result
    ) as mock_run:

        result = status.get_network_info()

    mock_run.assert_called_once_with(
        ["ip", "-brief", "addr"],
        capture_output=True,
        text=True
    )

    assert len(result) == 1

    assert result[0]["interface"] == "enp0s3"
    assert result[0]["state"] == "UP"
    assert result[0]["ipv4"] == "192.168.1.10/24"
    assert result[0]["ipv6"] == "fe80::1234/64"

def test_get_network_info_failure():
    from types import SimpleNamespace
    from unittest.mock import patch

    result = SimpleNamespace(
        returncode=1,
        stdout="",
        stderr="Command failed"
    )

    with patch("ash.status.subprocess.run", return_value=result):
        network = status.get_network_info()

    assert network == []

def test_get_network_info_skips_malformed_line():
    from types import SimpleNamespace
    from unittest.mock import patch

    fake_output = (
        "eth0 UP 192.168.1.10/24\n"
        "malformed\n"
    )

    mock_result = SimpleNamespace(
        returncode=0,
        stdout=fake_output,
        stderr=""
    )

    with patch(
        "ash.status.subprocess.run",
        return_value=mock_result
    ):
        result = status.get_network_info()

    assert len(result) == 1
    assert result[0]["interface"] == "eth0"


def test_get_network_info_skips_address_without_prefix():
    from types import SimpleNamespace
    from unittest.mock import patch

    fake_output = (
        "eth0 UP 192.168.1.10/24 invalid-address\n"
    )

    mock_result = SimpleNamespace(
        returncode=0,
        stdout=fake_output,
        stderr=""
    )

    with patch(
        "ash.status.subprocess.run",
        return_value=mock_result
    ):
        result = status.get_network_info()

    assert result == [
        {
            "interface": "eth0",
            "state": "UP",
            "ipv4": "192.168.1.10/24",
            "ipv6": None
        }
    ]

def test_get_disk_info():
    from types import SimpleNamespace
    from unittest.mock import patch

    fake_disk = SimpleNamespace(
        total=1000,
        used=400,
        free=600
    )

    with patch("ash.status.shutil.disk_usage", return_value=fake_disk):
        disk = status.get_disk_info()

    assert disk == {
        "total": 1000,
        "used": 400,
        "free": 600
    }

def test_get_cpu_times():
    from unittest.mock import mock_open, patch

    fake_stat = "cpu  100 20 30 850 10 5 0 0 0 0\n"

    with patch("builtins.open", mock_open(read_data=fake_stat)):
        cpu_times = status.get_cpu_times()

    assert cpu_times == (100, 20, 30, 850)

def test_get_cpu_usage():
    from unittest.mock import patch

    with patch(
        "ash.status.get_cpu_times",
        side_effect=[
            (100, 20, 30, 850),
            (120, 25, 35, 900)
        ]
    ):
        with patch("ash.status.time.sleep") as mock_sleep:
            usage = status.get_cpu_usage()

    mock_sleep.assert_called_once_with(1)

    assert usage == 37.5

def test_get_status_info():
    from unittest.mock import patch

    fake_memory = {
        "MemTotal": 8000,
        "MemFree": 2000,
        "MemAvailable": 6000,
        "SwapTotal": 4000,
        "SwapFree": 3000
    }

    fake_uptime = {
        "days": 1,
        "hours": 2,
        "minutes": 30,
        "seconds": 10
    }

    fake_disk = {
        "total": 10000,
        "used": 4000,
        "free": 6000
    }

    fake_network = [
        {
            "interface": "eth0",
            "state": "UP",
            "ipv4": "192.168.1.10/24",
            "ipv6": None
        }
    ]

    with patch("ash.status.get_memory_info", return_value=fake_memory), \
         patch("ash.status.get_uptime", return_value=fake_uptime), \
         patch("ash.status.get_disk_info", return_value=fake_disk), \
         patch("ash.status.get_cpu_info", return_value=4), \
         patch("ash.status.get_cpu_usage", return_value=25.0), \
         patch("ash.status.get_load_average", return_value={
             "1_minute": 0.5,
             "5_minutes": 0.4,
             "15_minutes": 0.3
         }), \
         patch("ash.status.get_network_info", return_value=fake_network):

        result = status.get_status_info()

    assert result["info"]["MemTotal"] == 8000
    assert result["info"]["MemFree"] == 2000
    assert result["info"]["MemAvailable"] == 6000

    assert result["uptime"] == fake_uptime
    assert result["disk"] == fake_disk
    assert result["cpu"] == 4
    assert result["cpu_usage"] == 25.0
    assert result["load_average"]["1_minute"] == 0.5
    assert result["network"] == fake_network

    assert result["memory_usage"] == 25.0
    assert result["swap_usage"] == 25.0
    assert result["disk_usage"] == 40.0
    assert result["health"] == "OK"

def test_show_status(capsys):
    from unittest.mock import patch

    fake_data = {
        "info": {
            "MemTotal": 8 * 1024 * 1024,
            "MemFree": 2 * 1024 * 1024,
            "MemAvailable": 6 * 1024 * 1024
        },
        "uptime": {
            "days": 1,
            "hours": 2,
            "minutes": 30,
            "seconds": 10
        },
        "disk": {
            "total": 10000,
            "used": 4000,
            "free": 6000
        },
        "cpu": 4,
        "cpu_usage": 25.0,
        "load_average": {
            "1_minute": 0.5,
            "5_minutes": 0.4,
            "15_minutes": 0.3
        },
        "network": [
            {
                "interface": "eth0",
                "state": "UP",
                "ipv4": "192.168.1.10/24",
                "ipv6": None
            }
        ],
        "memory_usage": 25.0,
        "swap_usage": 25.0,
        "disk_usage": 40.0,
        "health": "OK"
    }

    with patch("ash.status.get_status_info", return_value=fake_data):
        status.show_status(False)

    output = capsys.readouterr().out

    assert "Health: OK" in output
    assert "CPU: 4 logical CPUs" in output
    assert "CPU Usage: 25.00 %" in output
    assert "Memory Usage: 25.00 %" in output
    assert "Swap Usage: 25.00 %" in output
    assert "Disk Usage: 40.00 %" in output
    assert "Network: eth0 (UP)" in output
    assert "IPv4: 192.168.1.10/24" in output
    assert "Uptime: 1 days 2 hours 30 minutes 10 seconds" in output

def test_get_cpu_info():
    from unittest.mock import patch

    with patch("ash.status.os.cpu_count", return_value=8):
        result = status.get_cpu_info()

    assert result == 8


def test_calculate_cpu_usage_zero_delta():
    before = (100, 20, 30, 850)
    after = (100, 20, 30, 850)

    result = status.calculate_cpu_usage(before, after)

    assert result == 0.0


def test_calculate_health_critical():
    result = status.calculate_health(
        cpu_usage=95,
        memory_usage=50,
        disk_usage=50
    )

    assert result == "CRITICAL"

def test_calculate_memory_usage_without_swap():
    info = {
        "MemTotal": 1000000,
        "MemAvailable": 500000,
        "SwapTotal": 0,
        "SwapFree": 0
    }

    memory_usage, swap_usage = status.calculate_memory_usage(info)

    assert memory_usage == 50.0
    assert swap_usage == 0.0

def test_show_status_json(capsys):
    import json
    from unittest.mock import patch

    fake_data = {
        "info": {
            "MemTotal": 1000000,
            "MemFree": 200000,
            "MemAvailable": 500000
        },
        "uptime": {
            "days": 1,
            "hours": 2,
            "minutes": 30,
            "seconds": 15
        },
        "disk": {
            "total": 100000000,
            "used": 50000000,
            "free": 50000000
        },
        "cpu": 8,
        "cpu_usage": 25.0,
        "load_average": {
            "1_minute": 1.0,
            "5_minutes": 0.8,
            "15_minutes": 0.5
        },
        "network": [],
        "memory_usage": 50.0,
        "swap_usage": 0.0,
        "disk_usage": 50.0,
        "health": "OK"
    }

    with patch(
        "ash.status.get_status_info",
        return_value=fake_data
    ):
        status.show_status(True)

    output = capsys.readouterr().out

    result = json.loads(output)

    assert result == fake_data

def test_get_network_info_when_ip_command_missing():
    from unittest.mock import patch

    with patch(
        "ash.status.subprocess.run",
        side_effect=FileNotFoundError
    ):
        result = status.get_network_info()

    assert result == []
