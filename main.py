from cli_utils import parse_command, read_new_command, command_mapping
from graphics import (
    display_welcome,
    display_goodbye,
    display_segments,
    combine_segments,
    generate_panel,
    queue_notifications,
)
from classes import SystemConfig, Portfolio
from notifications import Notification, NotificationSource, NotificationManager

main_loop_continue = True


# Welcome graphics on startup.
display_welcome()

# Initilising system.
system_config = SystemConfig()
portfolio = Portfolio("Jack Woodman")
notification_manager = NotificationManager()

while system_config.main_loop_continue:
    input_display = combine_segments(
        generate_panel(), queue_notifications(notification_manager.get_notifications())
    )

    display_segments(input_display=input_display)

    new_command = read_new_command()
    command = parse_command(new_command)

    if command:
        notification_manager.add_notification(
            Notification(title="COMMAND RECOGNISED", subtitle=command.value, text=str(command))
        )

    try:
        command_mapping[command](system_config, portfolio, new_command[1:])
    except Exception as e:
        print(" - failed, command not supported", e)


system_config.freeze()
display_goodbye(system_config)
