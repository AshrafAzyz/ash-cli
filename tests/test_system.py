from ash import system
import platform


def test_get_system_info():
    data = system.get_system_info()

    # Check that all expected fields exist
    assert "os" in data
    assert "version" in data
    assert "codename" in data
    assert "kernel" in data
    assert "architecture" in data
    assert "python" in data
    assert "hostname" in data

    # Check actual values
    assert data["os"] == "Ubuntu"
    assert data["version"] == "26.04"
    assert data["codename"] == "resolute"

    # Check values against the Python environment
    assert data["kernel"] == platform.release()
    assert data["architecture"] == platform.machine()
    assert data["python"] == platform.python_version()
    assert data["hostname"] == platform.node()


def test_get_os_release():
    from unittest.mock import mock_open, patch

    fake_os_release = """NAME="Ubuntu"
VERSION_ID="26.04"
VERSION_CODENAME="resolute"
"""

    with patch(
        "builtins.open",
        mock_open(read_data=fake_os_release)
    ):
        result = system.get_os_release()

    assert result == {
        "NAME": "Ubuntu",
        "VERSION_ID": "26.04",
        "VERSION_CODENAME": "resolute"
    }

def test_get_system_info_mocked():
    from unittest.mock import patch

    fake_os_release = {
        "NAME": "TestOS",
        "VERSION_ID": "1.0",
        "VERSION_CODENAME": "test"
    }

    with patch(
        "ash.system.get_os_release",
        return_value=fake_os_release
    ), patch(
        "ash.system.platform.release",
        return_value="6.20.0-test"
    ), patch(
        "ash.system.platform.machine",
        return_value="x86_64"
    ), patch(
        "ash.system.platform.python_version",
        return_value="3.14.4"
    ), patch(
        "ash.system.platform.node",
        return_value="test-machine"
    ):

        result = system.get_system_info()

    assert result == {
        "os": "TestOS",
        "version": "1.0",
        "codename": "test",
        "kernel": "6.20.0-test",
        "architecture": "x86_64",
        "python": "3.14.4",
        "hostname": "test-machine"
    }

def test_show_system(capsys):
    from unittest.mock import patch

    fake_data = {
        "os": "Ubuntu",
        "version": "26.04",
        "codename": "resolute",
        "kernel": "6.20.0",
        "architecture": "x86_64",
        "python": "3.14.4",
        "hostname": "test-machine"
    }

    with patch(
        "ash.system.get_system_info",
        return_value=fake_data
    ):
        system.show_system(False)

    output = capsys.readouterr().out

    assert "OS: Ubuntu" in output
    assert "Version: 26.04" in output
    assert "Codename: resolute" in output
    assert "Kernel: 6.20.0" in output
    assert "Architecture: x86_64" in output
    assert "Python: 3.14.4" in output
    assert "Hostname: test-machine" in output

def test_show_system_json(capsys):
    from unittest.mock import patch
    import json

    fake_data = {
        "os": "Ubuntu",
        "version": "26.04",
        "codename": "resolute",
        "kernel": "6.20.0",
        "architecture": "x86_64",
        "python": "3.14.4",
        "hostname": "test-machine"
    }

    with patch(
        "ash.system.get_system_info",
        return_value=fake_data
    ):
        system.show_system(True)

    output = capsys.readouterr().out

    result = json.loads(output)

    assert result == fake_data
