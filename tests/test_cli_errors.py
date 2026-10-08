import sys

import pytest

from ash import cli


def test_help(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["ash", "--help"])

    with pytest.raises(SystemExit) as exc_info:
        cli.main()

    assert exc_info.value.code == 0

    captured = capsys.readouterr()

    assert "A Linux system information and management CLI." in captured.out
    assert "status" in captured.out
    assert "system" in captured.out
    assert "services" in captured.out


def test_unknown_argument(capsys, monkeypatch):
    monkeypatch.setattr(
        sys,
        "argv",
        ["ash", "status", "--unknown"]
    )

    with pytest.raises(SystemExit) as exc_info:
        cli.main()

    assert exc_info.value.code == 2

    captured = capsys.readouterr()

    assert "unrecognized arguments: --unknown" in captured.err


def test_mutually_exclusive_services(capsys, monkeypatch):
    monkeypatch.setattr(
        sys,
        "argv",
        ["ash", "services", "--failed", "--running"]
    )

    with pytest.raises(SystemExit) as exc_info:
        cli.main()

    assert exc_info.value.code == 2

    captured = capsys.readouterr()

    assert "not allowed with argument --failed" in captured.err
