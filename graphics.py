from classes import SystemConfig
version_number = "0.0.0"

def display_welcome():
    print("\nCLIP")
    print("command line interface portfolio")
    print("Jack Woodman, 2024.")
    print(f"version {version_number}\n")


def display_goodbye(system_config: SystemConfig):
    print(f"exiting program - uptime {system_config.uptime:.1f} seconds.")
