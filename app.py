from log import *
from config import config_get_current_settings_as_list


def _show_welcome_message():
    welcome_message = """\n\n
          /$$$$$$            /$$                    /$$$$$$      /$$$$$$$$
         /$$__  $$          | $$                   |_  $$_/     |__  $$__/
        | $$  \__/ /$$$$$$ /$$$$$$   /$$$$$$         | $$   /$$$$$$| $$   
        | $$ /$$$$/$$__  $|_  $$_/  /$$__  $$        | $$  /$$__  $| $$   
        | $$|_  $| $$  \ $$ | $$   | $$  \ $$        | $$ | $$  \ $| $$   
        | $$  \ $| $$  | $$ | $$ /$| $$  | $$        | $$ | $$  | $| $$   
        |  $$$$$$|  $$$$$$/ |  $$$$|  $$$$$$/       /$$$$$|  $$$$$$| $$   
         \______/ \______/   \___/  \______/       |______/\______/|__/   

                        SERVICE AMQP SAMPLES
                        --------------------
    \n"""
    settings_list = config_get_current_settings_as_list()
    print(welcome_message)
    print(f"\n{'#' * 80}\n")
    for setting in settings_list:
        print(f"# {setting}")
    print(f"\n{'#' * 80}\n\n")


def _init_application():
    info("Starting to run Service AMQP Samples")
    _show_welcome_message()


if __name__ == "__main__":
    _init_application()
