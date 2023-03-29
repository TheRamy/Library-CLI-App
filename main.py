import time
import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from typing import Optional

import util.formating
import util.db
import util.cli


console = Console()
app = typer.Typer()


@app.command("start")
def start():

    console.clear()

    typer.secho(f'''Welcome to Library CLI!\n\n
        You can execute command '--help' to see the possible commands''', fg=typer.colors.GREEN)
    # TODO: connect to database

    # util.formating.print_terminal('_') # this prints a line
    console.print(util.db.example_sql()[1])  # just an example


@app.command("sign_up")
def sign_up(username: str):
    console.clear()
    typer.echo(f"Nice that you are signing up!")
    # TODO: Add user with name {username} to database table

    util.cli.cli_add_user(username)


@app.command("sign_in")
def sign_in(username: str, password: str):
    console.clear()

    util.cli.cli_login(username, password)


@app.command("display_table")
def display_table():

    console.clear()

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Column 1", style="dim", width=10)
    table.add_column("Column 2", style="dim", min_width=10, justify=True)

    # util.db.example_table()
    table_db = util.db.sql_select("SELECT * FROM cool_table", "fetchall")
    for row in table_db:
        table.add_row(row[1], row[2])

    console.print(table)


if __name__ == "__main__":
    console.clear()
    app()
