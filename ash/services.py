# A service can be:
    # running continuously
    # started and then finished
    # stopped
    # failed
    # waiting for something

import subprocess

def show_services(failed_only, running_only):
    try:
        result = subprocess.run(
            [
                "systemctl",
                "list-units",
                "--type=service",
                "--no-pager",
                "--plain",
                "--no-legend"
            ],
            capture_output=True,
            text=True
        )
    except FileNotFoundError:
        print("systemctl is not available on this system.")
        return

    lines = result.stdout.splitlines()

    if result.returncode != 0:
        print("Failed to retrieve services.")
        print(result.stderr.strip())
        return

    total_count = 0
    active_count = 0
    failed_count = 0
    display_services = []

    for line in lines:
        parts = line.split(maxsplit=4)

        if parts and parts[0].endswith(".service"):
            total_count +=1
            if parts[2] == "active":
                active_count +=1
            if parts[2] == "failed":
                failed_count +=1
            if failed_only and parts[2] != "failed":
                continue
            if running_only and parts[2] != "active":
                continue
            display_services.append(parts)

    print(f"{'SERVICE':<40} {'ACTIVE':<7} {'SUB'}")
    print("_" * 40 + " " + "_" * 7 + " " + "_" * 3)

    for parts in display_services:
        print(f"{parts[0]:<40} {parts[2]:<7} {parts[3]}")

    print("\nService Summary")
    print("-" * 15)
    print(f"\nTotal: {total_count}")
    print(f"Active: {active_count}")
    print(f"Failed: {failed_count}\n")

    if failed_only and failed_count == 0:
        print("No failed services found")
    if running_only and active_count == 0:
        print("No running services found")
