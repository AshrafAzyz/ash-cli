# Contributing to ash-cli

Thank you for your interest in contributing to `ash-cli`.

`ash-cli` is currently maintained as a personal open-source project focused on Linux system information, Python CLI development, system administration, testing, and software engineering practices.

Contributions, bug reports, feature suggestions, documentation improvements, and other improvements are welcome.

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
├── README.md
├── CONTRIBUTING.md
├── LICENSE
├── pyproject.toml
└── .gitignore
```

### Main Modules

- `ash/cli.py` — command-line argument parsing and command dispatch
- `ash/status.py` — system resource and health information
- `ash/system.py` — operating system and system information
- `ash/services.py` — systemd service inspection

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
fix/service-filtering
fix/json-output
docs/update-installation
test/status-module
```

Keep changes focused. A pull request should ideally address one feature, bug, documentation change, or improvement at a time.

## Testing

`ash-cli` uses `pytest` for automated testing.

Run the test suite with:

```bash
python3 -m pytest
```

Before submitting a pull request, make sure all tests pass.

If you add new functionality, add or update tests where appropriate.

In addition to automated tests, manually verify CLI functionality affected by your changes.

For example:

```bash
ash status
ash system
ash services
```

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

## Pull Requests

Before opening a pull request:

1. Make sure the project installs successfully.
2. Run the test suite.
3. Verify the affected CLI commands manually.
4. Update the documentation if necessary.
5. Review the changes before submitting the pull request.

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
- Add comments when they provide useful context.
- Avoid comments that simply restate what the code already expresses.
- Add tests for new functionality where appropriate.
- Keep command-line output clear and consistent with existing commands.

## Documentation

Documentation is considered part of the project.

When adding or changing functionality, update the relevant documentation so that users and developers can understand the change.

Documentation may include:

- `README.md`
- Command help text
- `CONTRIBUTING.md`
- Documentation under `docs/`

When adding a new CLI command or option, document:

- The command or option name
- Its purpose
- How to use it
- Example usage
- Expected output, where useful

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

## Development Workflow

A typical development workflow is:

```text
Create a branch
      |
      v
Make changes
      |
      v
Run tests
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

## License

By contributing to `ash-cli`, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).
