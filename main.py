import typer
from rich.console import Console
from rich.table import Table
from typing import Optional

import util.formating
import util.db


console = Console()
app = typer.Typer()


@app.command("start")
def start():

    console.clear()

    typer.secho(f'''Welcome to Library CLI!\n\n
        You can execute command '--help' to see the possible commands''', fg=typer.colors.GREEN)
    # TODO: connect to database
    print(util.db.example_sql()[1]) # just an example 



@app.command("sign_up")
def sign_up(username: str): # This is how you can get arguments, here username is a mandatory argument for this command.
    console.clear()

    typer.echo(f"Nice that you are signing up!")
    # TODO: Add user with name {username} to database table

# Example function for tables, you can add more columns/row.


@app.command("display_table")
def display_table():

    console.clear()

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Column 1", style="dim", width=10)
    table.add_column("Column 2", style="dim", min_width=10, justify=True)

    table_db = util.db.example_table()
    for row in table_db:
        table.add_row(row[1], row[2])

    console.print(table)


if __name__ == "__main__":
    app()
