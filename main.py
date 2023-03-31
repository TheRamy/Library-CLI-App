import time
import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from typing import Optional
# import inquirer


import util.formating
import util.db
import util.cli
import util.session

console = Console()
app = typer.Typer()
session = util.session.load()  # Load user sessions (if not expired)


# this text will show when you call the --help command ~ramy
@app.callback()
def main():
    """
    Welcome to Library CLI.

    This is a project by Team2 that can be used by a public library, school or university.
    """

#######################################################
#######################################################
# ~~~~~ Commands that run without being logged in!~~~~~
#######################################################
#######################################################


@app.command("start")
def start():

    util.formating.show_header()

    # TODO: connect to database and create tables (if they don't exisit)

    typer.secho(f'''Welcome to Library CLI v0.1!\n\n
        You can execute command '--help' to see the possible commands''', fg=typer.colors.GREEN)
    print('')

    if session:
        typer.secho(
            f"Welcome back, {session['username']}!", fg=typer.colors.BRIGHT_YELLOW)
        print('')

        ##################################################################
        ##################################################################

        # choices_without_login   =['sign_up', 'search_by_name']
        # choices_with_login_only =['sign_up', 'search_by_name']

        # ask = [inquirer.List('run_command', message="What would you like to do?", choices=choices_without_login)]

        # answer = inquirer.prompt(ask)
        # #print(answer['run_command'])

        # if answer['run_command'] == "search_by_name":

        #     bookName = typer.prompt("What's the book name you're looking for?")
        #     search_by_name(f'{bookName}')

        ##################################################################
        ##################################################################

    else:
        typer.secho(f"You are not logged in!", fg=typer.colors.BRIGHT_YELLOW)
        print('')


@app.command("sign_up")
def sign_up(username: str):

    util.formating.show_header()

    typer.echo(f"Nice that you are signing up!")
    typer.echo(f"")
    util.cli.cli_add_user(username)
    typer.echo(f"")


@app.command("sign_in")
def sign_in(username: str, password: str):

    util.formating.show_header()

    username = util.cli.cli_login(username, password)
    typer.echo(f"")
    if username:
        # creates a session for the user
        session_id = util.session.login(username)
        # print (session_id)


@app.command("search_by_name")
def search_by_name(name: str):

    util.formating.show_header()

    table = Table(show_header=True, header_style="bold green")
    # table.add_column("Column 1", style="dim", width=10)
    table.add_column("#", style="dim", min_width=None, justify=True)
    table.add_column("Book ID", style="dim", min_width=None, justify=True)
    table.add_column("Name", style="dim", min_width=None, justify=True)
    table.add_column("Author", style="dim", min_width=None, justify=True)
    table.add_column("# Pages", style="dim", min_width=None, justify=True)
    table.add_column("Genre", style="dim", min_width=None, justify=True)
    table.add_column("Availability", style="dim", min_width=None, justify=True)

    # util.db.example_table()

    # Turning the book name to lower case
    # also, the sql query returns results in lower case. ~ramy
    name = name.lower()
    # table_db = util.db.sql_select(f"SELECT * from books WHERE lower(book_name) = '{name}'", "fetchall")
    table_db = util.db.sql_select(
        f"SELECT * from books WHERE lower(book_name) LIKE '%{name}%'", "fetchall")

    i = 1
    for row in table_db:
        table.add_row(str(i), str(row[0]), str(row[1]), str(
            row[2]), str(row[3]), str(row[4]), str(row[5]))
        i += 1

    typer.secho(
        f'You searched for a book named "{name}" so here is the result:', fg='white')
    console.print(table)
    console.print('')


# @app.command("display_table")
# def display_table():

#     console.clear()

#     table = Table(show_header=True, header_style="bold blue")
#     table.add_column("Column 1", style="dim", width=10)
#     table.add_column("Column 2", style="dim", min_width=10, justify=True)

#     # util.db.example_table()
#     table_db = util.db.sql_select("SELECT * FROM cool_table", "fetchall")
#     for row in table_db:
#         table.add_row(row[1], row[2])

#     console.print(table)

#######################################################
#######################################################
# Commands that require the user to be logged in first!
#######################################################
#######################################################
@app.command("add_book")
def add_book():

    util.formating.show_header()

    if session:

        typer.secho(f"Welcome back, {session['username']}!",  fg='green')

    else:
        typer.secho("You need to login first.",  fg='red')

#######################################################
#######################################################
# ~~~~~~~~~~~~~~~ THE END ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#######################################################
#######################################################


if __name__ == "__main__":
    console.clear()  # clears the terminal of any text.
    app()
