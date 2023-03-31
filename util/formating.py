
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

    # generated with font ANSI Regular from here:
    # https://patorjk.com/software/taag/#p=display&h=0&v=0&f=ANSI%20Regular&t=Library%20CLI

    typer.secho(f'''
██      ██ ██████  ██████   █████  ██████  ██    ██      ██████ ██      ██ 
██      ██ ██   ██ ██   ██ ██   ██ ██   ██  ██  ██      ██      ██      ██ 
██      ██ ██████  ██████  ███████ ██████    ████       ██      ██      ██ 
██      ██ ██   ██ ██   ██ ██   ██ ██   ██    ██        ██      ██      ██ 
███████ ██ ██████  ██   ██ ██   ██ ██   ██    ██         ██████ ███████ ██ 
    ''', fg=typer.colors.GREEN)

    # print('')
    # print_terminal("_")


def print_table(headers, table_db):
    """Provide a list with header names you want and 
    the result of the sql query result (fetchall) and 
    it will return the table. ~ramy
      """
    
    table = Table(show_header=True, header_style="bold green")
    for header in headers:
        table.add_column(header, style="dim", min_width=None, justify=True)

    i = 1
    for row in table_db:
        row_data = [str(col) for col in row]
        table.add_row(str(i), *row_data)
        i += 1

    console.print(table)

