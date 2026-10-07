import argparse
import status
import system
import services

parser = argparse.ArgumentParser(description = "A Linux system information CLI.")

subparsers = parser.add_subparsers(dest="command")

subparsers.add_parser(
	"status",
	help="Show system health information",
	description="Display CPU, memory, disk, uptime, and general system health."
)

subparsers.add_parser(
	"system",
	help="Show system information"
)

services_parser = subparsers.add_parser(
	"services",
	help="Show systemd services"
)

services_parser.add_argument(
    "--failed",
    action="store_true",
    help="Show only failed services"
)

args = parser.parse_args()

if args.command == "status":
	status.show_status()
elif args.command == "system":
	system.show_system()
elif args.command == "services":
	services.show_services(args.failed)
