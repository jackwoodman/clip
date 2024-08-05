from cli_utils import parse_command, read_new_command, command_mapping
from graphics import display_welcome, display_goodbye
from classes import SystemConfig, Portfolio
from notifications import Notification, NotificationSource, NotificationManager
main_loop_continue = True



display_welcome()


# initialise
system_config = SystemConfig()
portfolio = Portfolio("Jack Woodman")

while system_config.main_loop_continue:
    new_command = read_new_command()
    command = parse_command(new_command)

    print(f"recognised command: {command}")
    try:
        command_mapping[command](system_config, portfolio, new_command[1:])
    except Exception as e:
        print(" - failed, command not supported", e)

    




system_config.freeze()
display_goodbye(system_config)