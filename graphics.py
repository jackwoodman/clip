from classes import SystemConfig
version_number = "0.0.0"

panel_width= 90
notif_width = 44
total_width = 145
segment_height = 40
total_height = 50

def panel_filler():
    import random
    return [(" "*(panel_width - 1))for i in range(segment_height - 1)]

def notif_filler():
    import random
    return [("#"*(notif_width - 1)) for i in range(segment_height - 1)]

def combine_segments(panel_segment: list[str], notification_segment: list[str]) -> list[str]:
    output_segment = ["|" +str(panel_line)+ "|" + notification_line+"|" for panel_line, notification_line in zip(panel_segment, notification_segment)]

    return output_segment


def display_segments(input_display):
    for i in input_display:
        print(i)

display_segments(combine_segments(panel_filler(), notif_filler()))



def display_welcome():
    print("\nCLIP")
    print("command line interface portfolio")
    print("Jack Woodman, 2024.")
    print(f"version {version_number}\n")


def display_goodbye(system_config: SystemConfig):
    print(f"exiting program - uptime {system_config.uptime:.1f} seconds.")
