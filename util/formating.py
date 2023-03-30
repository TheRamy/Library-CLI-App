
import os
import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from typing import Optional

console = Console()


def print_terminal(char_to_print):
    """Fills ONE line in the terminal with one character. For example "----------". ~ramy"""
    cols, rows = os.get_terminal_size()
    dashes = f'{char_to_print}' * cols
    print(dashes, end='', flush=True)


def show_header():
    """To show the same header on each command. ~ramy"""

    console.clear()

    # Generated using font "big" using:
    #  https://patorjk.com/software/taag/#p=display&h=0&v=2&f=Big&t=Library%20CLI
#     typer.secho(f'''
#   _        _   _                                        _____   _        _____
#  | |      (_) | |                                      / ____| | |      |_   _|
#  | |       _  | |__    _ __    __ _   _ __   _   _    | |      | |        | |
#  | |      | | | '_ \  | '__|  / _` | | '__| | | | |   | |      | |        | |
#  | |____  | | | |_) | | |    | (_| | | |    | |_| |   | |____  | |____   _| |_
#  |______| |_| |_.__/  |_|     \__,_| |_|     \__, |    \_____| |______| |_____|
#                                               __/ |
#                                              |___/
#     ''', fg=typer.colors.BRIGHT_WHITE)

    # generated with font ANSI Regular from here:
    # https://patorjk.com/software/taag/#p=display&h=0&v=0&f=ANSI%20Regular&t=Library%20CLI

    typer.secho(f'''
██      ██ ██████  ██████   █████  ██████  ██    ██      ██████ ██      ██ 
██      ██ ██   ██ ██   ██ ██   ██ ██   ██  ██  ██      ██      ██      ██ 
██      ██ ██████  ██████  ███████ ██████    ████       ██      ██      ██ 
██      ██ ██   ██ ██   ██ ██   ██ ██   ██    ██        ██      ██      ██ 
███████ ██ ██████  ██   ██ ██   ██ ██   ██    ██         ██████ ███████ ██ 
    ''', fg=typer.colors.BRIGHT_GREEN)

    # print('')
    # print_terminal("_")
