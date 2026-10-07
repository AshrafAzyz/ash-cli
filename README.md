# ash-cli

A lightweight Linux system information CLI written in Python.

`ash-cli` is a personal open-source project built to explore Linux system information, Python CLI development, system administration, and software engineering practices.

The project is being developed on Ubuntu Linux and is designed to provide a simple command-line interface for inspecting and monitoring a Linux system.

---

## 🚧 Project Status

**Early development**

Currently implemented:

- System information
- CPU information
- Memory information
- Swap usage
- Disk usage
- System uptime
- Systemd service inspection
- Command-line argument parsing
- JSON output
- Mutually exclusive command options

Planned features include:

- Improved system health monitoring
- More detailed systemd service information
- Better error handling
- Automated testing with `pytest`
- Python package structure
- Installation through `pip`
- Linux package support
- Continuous integration
- Improved documentation

---

## ✨ Features

### System Information

Display basic information about the Linux system:

```bash
python3 ash.py system
