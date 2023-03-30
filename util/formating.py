
import os
import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from typing import Optional

console = Console()



def print_terminal(char_to_print):
    """Fills ONE line in the terminal with one character. For example "----------". """
    cols, rows = os.get_terminal_size()
    dashes = f'{char_to_print}' * cols
    print(dashes, end='', flush=True)


def show_header():

    console.clear()

    typer.secho(f'''Welcome to Library CLI!
    v0.1''', fg=typer.colors.CYAN)

    print ('')
