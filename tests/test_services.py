from types import SimpleNamespace
from unittest.mock import patch

from ash import services


def make_fake_result(output, returncode=0, error=""):
    return SimpleNamespace(
        returncode=returncode,
        stdout=output,
        stderr=error
    )


def test_show_services(capsys):
    fake_output = """foo.service loaded active running Foo Service
bar.service loaded active exited Bar Service
broken.service loaded failed failed Broken Service
"""

    fake_result = make_fake_result(fake_output)

    with patch(
        "ash.services.subprocess.run",
        return_value=fake_result
    ):
        services.show_services(False, False)

    captured = capsys.readouterr()

    assert "foo.service" in captured.out
    assert "bar.service" in captured.out
    assert "broken.service" in captured.out

    assert "Total: 3" in captured.out
    assert "Active: 2" in captured.out
    assert "Failed: 1" in captured.out


def test_show_failed_services(capsys):
    fake_output = """foo.service loaded active running Foo Service
bar.service loaded active exited Bar Service
broken.service loaded failed failed Broken Service
"""

    fake_result = make_fake_result(fake_output)

    with patch(
        "ash.services.subprocess.run",
        return_value=fake_result
    ):
        services.show_services(True, False)

    captured = capsys.readouterr()

    assert "broken.service" in captured.out
    assert "foo.service" not in captured.out
    assert "bar.service" not in captured.out

    # Summary should still describe the whole system
    assert "Total: 3" in captured.out
    assert "Active: 2" in captured.out
    assert "Failed: 1" in captured.out


def test_show_running_services(capsys):
    fake_output = """foo.service loaded active running Foo Service
bar.service loaded active exited Bar Service
broken.service loaded failed failed Broken Service
"""

    fake_result = make_fake_result(fake_output)

    with patch(
        "ash.services.subprocess.run",
        return_value=fake_result
    ):
        services.show_services(False, True)

    captured = capsys.readouterr()

    assert "foo.service" in captured.out
    assert "bar.service" in captured.out
    assert "broken.service" not in captured.out

    # Summary should still describe the whole system
    assert "Total: 3" in captured.out
    assert "Active: 2" in captured.out
    assert "Failed: 1" in captured.out


def test_systemctl_failure(capsys):
    fake_result = make_fake_result(
        output="",
        returncode=1,
        error="Failed to communicate with systemd."
    )

    with patch(
        "ash.services.subprocess.run",
        return_value=fake_result
    ):
        services.show_services(False, False)

    captured = capsys.readouterr()

    assert "Failed to retrieve services." in captured.out
    assert "Failed to communicate with systemd." in captured.out

def test_failed_filter_with_no_failed_services(capsys):
    from types import SimpleNamespace
    from unittest.mock import patch

    fake_output = (
        "ssh.service loaded active running SSH Server\n"
        "cron.service loaded active running Cron Service\n"
    )

    mock_result = SimpleNamespace(
        returncode=0,
        stdout=fake_output,
        stderr=""
    )

    with patch("ash.services.subprocess.run", return_value=mock_result):
        services.show_services(True, False)

    output = capsys.readouterr().out

    assert "No failed services found" in output


def test_running_filter_with_no_running_services(capsys):
    from types import SimpleNamespace
    from unittest.mock import patch

    fake_output = (
        "failed.service loaded failed failed Some Service\n"
    )

    mock_result = SimpleNamespace(
        returncode=0,
        stdout=fake_output,
        stderr=""
    )

    with patch("ash.services.subprocess.run", return_value=mock_result):
        services.show_services(False, True)

    output = capsys.readouterr().out

    assert "No running services found" in output

def test_systemctl_not_available(capsys):
    with patch(
        "ash.services.subprocess.run",
        side_effect=FileNotFoundError
    ):
        services.show_services(False, False)

    captured = capsys.readouterr()

    assert "systemctl is not available on this system." in captured.out
