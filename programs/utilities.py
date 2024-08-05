from classes import SystemConfig, Portfolio, CommandArgs
def quit_clip(system_config: SystemConfig, _: Portfolio, __: CommandArgs):
    system_config.main_loop_continue = False
    return system_config
    