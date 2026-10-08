import argparse

from . import status
from . import system
from . import services


def main():
    parser = argparse.ArgumentParser(
        description="A Linux system information CLI."
    )

    subparsers = parser.add_subparsers(dest="command")

    status_parser = subparsers.add_parser(
        "status",
        help="Show system health information",
        description="Display CPU, memory, disk, uptime, and general system health."
    )

    status_parser.add_argument(
        "--json",
        dest="json",
        action="store_true",
        help="Output status information as JSON"
    )

    system_parser = subparsers.add_parser(
        "system",
        help="Show system information"
    )

    system_parser.add_argument(
        "--json",
        dest="json",
        action="store_true",
        help="Output system information as JSON"
    )

    services_parser = subparsers.add_parser(
        "services",
        help="Show systemd services"
    )

    services_group = services_parser.add_mutually_exclusive_group()

    services_group.add_argument(
        "--failed",
        dest="failed",
        action="store_true",
        help="Show only failed services"
    )

    services_group.add_argument(
        "--running",
        dest="running",
        action="store_true",
        help="Show only running services"
    )

    args = parser.parse_args()

    if args.command == "status":
        status.show_status(args.json)

    elif args.command == "system":
        system.show_system(args.json)

    elif args.command == "services":
        services.show_services(args.failed, args.running)


if __name__ == "__main__":
    main()
