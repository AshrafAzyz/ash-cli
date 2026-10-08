# Contributing to ash-cli

Thank you for your interest in contributing to `ash-cli`.

`ash-cli` is an open-source project focused on Linux system information, Python CLI development, system administration, testing, software packaging, and open-source software engineering practices.

Contributions, bug reports, feature suggestions, documentation improvements, tests, and other improvements are welcome.

## Development Setup

### Requirements

- Linux
- Python 3.14 or later
- Git
- `systemd` for service-related functionality

### Clone the Repository

Clone the repository and enter the project directory:

```bash
git clone https://github.com/AshrafAzyz/ash-cli.git
cd ash-cli
```

### Create a Virtual Environment

Create a Python virtual environment:

```bash
python3 -m venv .venv
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

### Install the Project

Install `ash-cli` in editable mode:

```bash
python3 -m pip install -e .
```

Editable installation allows changes to the source code to be used immediately during development without reinstalling the project after every change.

Verify the installation:

```bash
ash --version
ash --help
```

## Project Structure

The project uses a Python package structure:

```text
ash-cli/
├── ash/
│   ├── __init__.py
│   ├── cli.py
│   ├── status.py
│   ├── system.py
│   └── services.py
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

### Main Modules

- `ash/cli.py` — command-line argument parsing, command options, and command dispatch
- `ash/status.py` — system resource information and system health assessment
- `ash/system.py` — operating system and system information
- `ash/services.py` — systemd service inspection and service filtering

### Test Modules

- `tests/test_cli.py` — CLI command and argument behavior
- `tests/test_cli_errors.py` — CLI error handling
- `tests/test_status.py` — system status calculations and output
- `tests/test_system.py` — system information behavior
- `tests/test_services.py` — systemd service behavior and error handling

## Making Changes

Create a new branch for your changes instead of working directly on `main`.

For example:

```bash
git checkout -b feature/add-package-info
```

Use a descriptive branch name that explains the purpose of the change.

Examples:

```text
feature/add-package-info
feature/add-version-command
feature/add-json-output
fix/service-filtering
fix/system-information
docs/update-installation
test/status-module
```

Keep changes focused. A pull request should ideally address one feature, bug, documentation change, test improvement, or other related improvement at a time.

Avoid mixing unrelated changes in the same pull request.

## Testing

`ash-cli` uses `pytest` for automated testing.

Run the complete test suite:

```bash
python3 -m pytest -v
```

Run the tests with coverage:

```bash
python3 -m pytest --cov=ash --cov-report=term-missing
```

The project currently contains 44 automated tests covering:

- CLI commands
- CLI errors
- System information
- System status
- CPU calculations
- Memory calculations
- Disk calculations
- Network information
- systemd services
- Service filtering
- Error handling
- JSON output

Before submitting a pull request, make sure all tests pass.

If you add new functionality, add or update tests where appropriate.

### Manual CLI Testing

Automated tests should be complemented by manual testing of affected functionality.

For example:

```bash
ash status
ash status --json

ash system
ash system --json

ash services
ash services --failed
ash services --running
```

When changing command-line behavior, also verify the relevant help output:

```bash
ash --help
ash status --help
ash system --help
ash services --help
```

## Error Handling

`ash-cli` should handle expected system limitations gracefully.

For example, functionality that depends on `systemctl` should not cause an unhandled `FileNotFoundError` when `systemctl` is unavailable.

Similarly, optional information should not cause the application to crash when it is unavailable on a particular Linux distribution.

When adding new functionality:

- Handle expected operating-system errors.
- Provide clear error messages.
- Avoid exposing unnecessary implementation details to users.
- Add tests for important error conditions.

## Commit Guidelines

Write clear and concise commit messages.

Use imperative language such as:

```text
Add package information command
Fix service filtering
Improve system status output
Add tests for system information
Update project documentation
```

Avoid vague commit messages such as:

```text
update
changes
fix stuff
more changes
```

A commit should ideally represent one logical change.

For example, a commit that adds a new feature should not also contain unrelated formatting changes or unrelated documentation updates.

## Pull Requests

Before opening a pull request:

1. Make sure the project installs successfully.
2. Run the complete test suite.
3. Verify affected CLI commands manually.
4. Verify relevant help output.
5. Update documentation if necessary.
6. Review the changes before submitting the pull request.
7. Make sure unrelated files or changes are not included.

A pull request should describe:

- What was changed
- Why the change was made
- How the change was tested
- Any known limitations or issues

Keep pull requests focused and avoid including unrelated changes.

## Code Style

When contributing code:

- Use clear and descriptive names.
- Keep functions focused on a specific responsibility.
- Avoid unnecessary complexity.
- Follow the existing project structure.
- Keep command-line output clear and consistent.
- Use comments when they provide useful context.
- Avoid comments that simply restate what the code already expresses.
- Add tests for new functionality where appropriate.
- Reuse existing functions when appropriate instead of duplicating logic.
- Prefer clear and maintainable Python code over overly clever implementations.

## Command-Line Design

When adding a new command or option, consider consistency with the existing CLI.

For example:

```bash
ash status
ash system
ash services
```

Options should have clear names and help descriptions.

For example:

```bash
ash status --json
ash system --json
ash services --failed
ash services --running
```

If multiple options cannot logically be used together, they should be implemented as mutually exclusive options.

Command-line behavior should be predictable and consistent across the project.

## Documentation

Documentation is considered part of the project.

When adding or changing functionality, update the relevant documentation so that users and developers can understand the change.

Documentation may include:

- `README.md`
- `CONTRIBUTING.md`
- Command help text
- Documentation under `docs/`

When adding a new CLI command or option, document:

- The command or option name
- Its purpose
- How to use it
- Example usage
- Expected output, where useful

If a feature changes existing behavior, update the existing documentation instead of creating conflicting documentation.

## Reporting Bugs

When reporting a bug, provide enough information to reproduce it.

Where possible, include:

- Operating system and version
- Python version
- `ash-cli` version
- Command that was executed
- Expected behavior
- Actual behavior
- Relevant error output

For example:

```text
Operating system: Ubuntu 26.04
Python: 3.14.4
ash-cli: 0.1.0
Command: ash services --failed

Expected:
Failed services are displayed.

Actual:
An error message is displayed.
```

Avoid including sensitive information such as:

- Passwords
- Private keys
- API tokens
- Authentication credentials
- Personal information
- Other private information

## Feature Requests

Feature requests are welcome.

When proposing a feature, describe:

- The problem the feature would solve
- The proposed behavior
- Example command usage, if applicable
- Any relevant implementation considerations

For example:

```text
Feature: Display APT package information

Problem:
Users currently cannot inspect package information through ash.

Proposed command:
ash packages <package-name>

Example:
ash packages python3
```

Feature requests should focus on a clear user or development need.

## Development Workflow

A typical development workflow is:

```text
Create a branch
     |
     v
Make changes
     |
     v
Add or update tests
     |
     v
Run automated tests
     |
     v
Test the CLI manually
     |
     v
Update documentation
     |
     v
Review changes
     |
     v
Commit changes
     |
     v
Push branch
     |
     v
Open pull request
```

Before pushing changes, it is recommended to check the working tree:

```bash
git status
```

Review the changes:

```bash
git diff
```

Review staged changes before committing:

```bash
git diff --cached
```

## Git Guidelines

Do not commit generated or environment-specific files.

The repository should not include files such as:

```text
.venv/
__pycache__/
*.pyc
.pytest_cache/
*.egg-info/
.coverage
```

These files are excluded through `.gitignore`.

Before committing, check:

```bash
git status
```

If an unwanted generated file appears in the working tree, remove it or update `.gitignore` before committing.

## License

By contributing to `ash-cli`, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).
