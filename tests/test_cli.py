from unittest.mock import patch
import sys
import pytest
from ash import cli


def test_status_command():
    with patch("ash.cli.status.show_status") as mock_status:
        with patch("sys.argv", ["ash", "status"]):
            cli.main()

    mock_status.assert_called_once_with(False)


def test_status_json_command():
    with patch("ash.cli.status.show_status") as mock_status:
        with patch("sys.argv", ["ash", "status", "--json"]):
            cli.main()

    mock_status.assert_called_once_with(True)


def test_system_command():
    with patch("ash.cli.system.show_system") as mock_system:
        with patch("sys.argv", ["ash", "system"]):
            cli.main()

    mock_system.assert_called_once_with(False)


def test_system_json_command():
    with patch("ash.cli.system.show_system") as mock_system:
        with patch("sys.argv", ["ash", "system", "--json"]):
            cli.main()

    mock_system.assert_called_once_with(True)


def test_services_command():
    with patch("ash.cli.services.show_services") as mock_services:
        with patch("sys.argv", ["ash", "services"]):
            cli.main()

    mock_services.assert_called_once_with(False, False)


def test_services_failed_command():
    with patch("ash.cli.services.show_services") as mock_services:
        with patch("sys.argv", ["ash", "services", "--failed"]):
            cli.main()

    mock_services.assert_called_once_with(True, False)


def test_services_running_command():
    with patch("ash.cli.services.show_services") as mock_services:
        with patch("sys.argv", ["ash", "services", "--running"]):
            cli.main()

    mock_services.assert_called_once_with(False, True)

def test_version(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["ash", "--version"])

    with pytest.raises(SystemExit) as exc_info:
        cli.main()

    assert exc_info.value.code == 0

    captured = capsys.readouterr()

    assert captured.out.strip() == "ash 0.1.0"
