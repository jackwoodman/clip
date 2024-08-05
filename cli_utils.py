from classes import Command
from typing import Optional
import difflib
from programs.utilities import quit_clip
from programs.portfolio import buy, sell


RawCommand = list[str]





command_mapping = {
    Command.QUIT: quit_clip,
    Command.BUY: buy,
    Command.SELL: sell,
    Command.JOEY: print
}

def get_closest_match(input_str: str, acceptable_strings: list[str]) -> str:
    comparison_ratios = [(candidate_str, difflib.SequenceMatcher(None, input_str, candidate_str).ratio()) for candidate_str in acceptable_strings]
    comparison_ratios.sort(reverse=True, key=lambda x: x[1])

    return comparison_ratios[0]


def prompt_user_bool(prompt_text: str) -> bool:
    return input(f"{prompt_text} ").lower() == "yes"

def tell_user_text(notification_text):
    print(notification_text)




def read_new_command(prompt: str = ">") -> RawCommand:
    """
    Read command from CLI, and return as a raw command.
    """

    return input(f"{prompt} ").split(" ")


def parse_command(input_command: RawCommand, command_assist: bool = True) -> Optional[Command]:
    """
    Attempt to match against known commands.
    """

    root_command = input_command[0]

    try:
        return Command(root_command)
    
    except ValueError:

        if command_assist:
            acceptable_commands = Command._value2member_map_.keys()

            best_match = get_closest_match(root_command, acceptable_commands)[0]

            if prompt_user_bool(f"Did you mean '{best_match}'?"):      
                return Command(best_match)
            else:
                tell_user_text(f"Could not match input '{root_command}' against known commands.")
        else:
            tell_user_text(f"Command '{root_command}' not currently supported.")
    
    return None



    







