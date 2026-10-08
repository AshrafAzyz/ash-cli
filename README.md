# ash-cli

A lightweight Linux system information and administration CLI written in Python.

`ash-cli` is an open-source project developed to explore Linux system programming, Python CLI development, system administration, software packaging, testing, and open-source software engineering practices.

The project is developed on Ubuntu Linux and provides a command-line interface for inspecting system information, monitoring basic system health, and inspecting systemd services.

## Project Status

**Early development**

The core CLI architecture is currently implemented and the project is being expanded incrementally.

Current capabilities include:

- System information
- CPU information and usage
- Memory information and usage
- Swap usage
- Disk usage
- System uptime
- Load average
- Network interface information
- Basic system health assessment
- systemd service inspection
- Failed service filtering
- Running service filtering
- JSON output
- Mutually exclusive command options
- Python package structure
- Editable installation through `pip`
- Automated testing with `pytest`

Planned development includes:

- Improved error handling
- More detailed systemd information
- Package and APT management
- Configuration support
- Logging
- Expanded test coverage
- Continuous integration
- Linux package distribution
- Improved documentation

## Features

### System Information

Display basic information about the Linux system:

```bash
ash system
