```markdown
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
- Graceful handling of unavailable Linux system utilities
- Graceful handling of missing optional system information
- Automated testing with `pytest`
- 44 passing automated tests

Planned development includes:

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
```

Example output:

```text
OS: Ubuntu
Version: 26.04
Codename: resolute
Kernel: 6.20.0
Architecture: x86_64
Python: 3.14.4
Hostname: ashraf-VirtualBox
```

JSON output is also supported:

```bash
ash system --json
```

Example output:

```json
{
    "os": "Ubuntu",
    "version": "26.04",
    "codename": "resolute",
    "kernel": "6.20.0",
    "architecture": "x86_64",
    "python": "3.14.4",
    "hostname": "ashraf-VirtualBox"
}
```

### System Status

Display basic system health information:

```bash
ash status
```

Example output:

```text
Health: OK
---
CPU: 4 logical CPUs
CPU Usage: 12.45 %
Load Average: 0.42, 0.38, 0.31
---
Memory Total: 7.65 GiB
Memory Free: 2.14 GiB
Memory Available: 4.82 GiB
Memory Usage: 37.03 %
---
Swap Usage: 0.00 %
Disk Usage: 28.51 %
---
Network: enp0s3 (UP)
IPv4: 192.168.1.10/24
IPv6: fe80::1234/64
---
Uptime: 2 days 4 hours 31 minutes 12 seconds
```

JSON output is also supported:

```bash
ash status --json
```

### Systemd Services

List systemd services:

```bash
ash services
```

Example output:

```text
SERVICE                                  ACTIVE  SUB
________________________________________ _______ ___
NetworkManager.service                   active  running
ssh.service                              active  running
vboxadd.service                          failed  failed

Service Summary
---------------

Total: 64
Active: 63
Failed: 1
```

Show only failed services:

```bash
ash services --failed
```

Show only running services:

```bash
ash services --running
```

The `--failed` and `--running` options are mutually exclusive.

If `systemctl` is unavailable on the system, `ash` reports the problem gracefully instead of crashing.

## Command Overview

| Command | Description |
|---|---|
| `ash --help` | Display general help |
| `ash --version` | Display the installed version |
| `ash system` | Display system information |
| `ash system --json` | Display system information as JSON |
| `ash status` | Display system health information |
| `ash status --json` | Display system health information as JSON |
| `ash services` | List systemd services |
| `ash services --failed` | Show failed services |
| `ash services --running` | Show running services |

## Installation

### Development Installation

Clone the repository:

```bash
git clone https://github.com/AshrafAzyz/ash-cli.git
cd ash-cli
```

Create a Python virtual environment:

```bash
python3 -m venv .venv
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Install the project in editable mode:

```bash
pip install -e .
```

The `-e` option installs the project in editable mode, allowing changes to the source code to be reflected immediately without reinstalling the package.

Verify the installation:

```bash
ash --version
```

## Development

The project follows a modular Python package structure:

```text
ash-cli/
├── ash/
│   ├── __init__.py
│   ├── cli.py
│   ├── services.py
│   ├── status.py
│   └── system.py
├── tests/
│   ├── test_cli.py
│   ├── test_cli_errors.py
│   ├── test_services.py
│   ├── test_status.py
│   └── test_system.py
├── README.md
├── CONTRIBUTING.md
├── LICENSE
├── pyproject.toml
└── .gitignore
```

### Source Modules

#### `ash/cli.py`

Handles:

- Argument parsing
- Subcommands
- Command-line options
- Version information
- Dispatching commands to the appropriate modules

#### `ash/status.py`

Handles:

- CPU information
- CPU usage
- Memory information
- Swap usage
- Disk usage
- Load average
- Network information
- Uptime
- System health assessment

#### `ash/system.py`

Handles:

- Operating system information
- Linux distribution version
- Distribution codename
- Kernel version
- CPU architecture
- Python version
- Hostname

#### `ash/services.py`

Handles:

- systemd service discovery
- Active service filtering
- Failed service filtering
- Service summaries
- Handling systems where `systemctl` is unavailable

## Testing

Tests are written using `pytest`.

Run the complete test suite:

```bash
python3 -m pytest -v
```

Run tests with coverage:

```bash
python3 -m pytest --cov=ash --cov-report=term-missing
```

The project currently contains **44 automated tests** covering:

- CLI commands
- CLI errors
- System information
- System status
- Network information
- CPU calculations
- Memory calculations
- Disk calculations
- systemd services
- Error handling
- JSON output

## Error Handling

`ash-cli` is designed to handle missing system functionality gracefully where possible.

For example, if `systemctl` is unavailable:

```text
systemctl is not available on this system.
```

If a Linux distribution does not provide `VERSION_CODENAME`, the value is represented as unavailable instead of causing the command to terminate with a `KeyError`.

## Project Goals

The long-term goal of `ash-cli` is to develop a practical Linux command-line tool while providing hands-on experience with:

- Python application architecture
- Linux system interfaces
- Command-line application development
- systemd
- APT and Debian package management
- Python packaging
- Automated testing
- Git and GitHub
- Continuous integration
- Open-source development
- Linux software distribution

## Contributing

Contributions, suggestions, and bug reports are welcome.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting changes.

## License

This project is licensed under the MIT License.

See [LICENSE](LICENSE) for details.

## Repository

GitHub:

https://github.com/AshrafAzyz/ash-cli
```
