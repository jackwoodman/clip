from classes import SystemConfig
from notifications import Notification

version_number = "0.0.0"

panel_width = 90
notif_width = 44
total_width = 145
segment_height = 40
total_height = 50

empty_notification = Notification("", "", "")


def combine_segments(panel_segment: list[str], notification_segment: list[str]) -> list[str]:
    # DEBUG CODE
    while len(notification_segment) < segment_height:
        notification_segment.append(" ")

    output_segment = [
        "|" + str(panel_line).ljust(panel_width - 1) + "|" + notification_line.ljust(notif_width - 1) + "|"
        for panel_line, notification_line in zip(panel_segment, notification_segment)
    ]

    return output_segment


def display_segments(input_display):
    for i in input_display[::-1]:
        print(i)
    print("-" * total_width)


def generate_panel():
    return [" " for _ in range(segment_height)]


def queue_notifications(new_notifications: list[Notification]):
    output_text = []

    for notification in new_notifications:
        # First, calculate text wrapping.
        notif_text = notification.text
        chunks, chunk_size = len(notif_text), len(notif_text) // (notif_width - 1)

        if chunk_size == 0:
            chunk_size = len(notif_text)

        split_text = [notif_text[i : i + chunk_size] for i in range(0, chunks, chunk_size)]

        for text in split_text:
            output_text.append(text)

        if notification.subtitle:
            output_text.append(notification.subtitle)

        output_text.append(notification.title)

        output_text.append(" ")

    return output_text


def display_welcome():
    print("\nCLIP")
    print("command line interface portfolio")
    print("Jack Woodman, 2024.")
    print(f"version {version_number}\n")


def display_goodbye(system_config: SystemConfig):
    print(f"exiting program - uptime {system_config.uptime:.1f} seconds.")
