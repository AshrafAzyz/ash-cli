from ash import system

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
    data = system.get_os_release()

    assert "NAME" in data
    assert "VERSION_ID" in data
    assert "VERSION_CODENAME" in data

    assert data["NAME"] == "Ubuntu"
    assert data["VERSION_ID"] == "26.04"
    assert data["VERSION_CODENAME"] == "resolute"
