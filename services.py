# A service can be:
    # running continuously
    # started and then finished
    # stopped
    # failed
    # waiting for something

import subprocess

def show_services(failed_only):
    result = subprocess.run(["systemctl", "list-units" ,"--type=service", "--no-pager", "--plain", "--no-legend"], capture_output=True, text=True)
    lines = result.stdout.splitlines()

    if result.returncode != 0:
        print("Failed to retrieve services.")
        print(result.stderr.strip())
        return

    print(f"{'SERVICE':<40} {'ACTIVE':<7} {'SUB'}")
    print("_" * 40 + " " + "_" * 7 + "_" * 7)

    for line in lines:
        parts = line.split(maxsplit=4)

        if parts and parts[0].endswith(".service"):
            if failed_only and parts[2] != "failed":
                continue
                
            print(f"{parts[0]:<40} {parts[2]:<7} {parts[3]}")
