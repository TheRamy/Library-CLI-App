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

    search_result = util.db.sql_select(
        f"SELECT * from books WHERE lower(book_name) LIKE lower('%{name}%')", "fetchall")

    if search_result:

        typer.secho(
            f'You searched for a book with the name "{name}" so here is the result:', fg='white')

        table_headers = ['#', 'Book ID', 'Name',
                         'Author', '# Pages', 'Genre', 'Availability']
        util.formating.print_table(table_headers, search_result)
        console.print('')
    else:
        typer.secho(
            f'No book  with the name "{name}" could be found. Try again!', fg='white')
        console.print('')


@app.command("search_by_author")
def search_by_author(author: str):

    util.formating.show_header()

    search_result = util.db.sql_select(
        f"SELECT * from books WHERE lower(book_author) LIKE lower('%{author}%')", "fetchall")

    if search_result:

        typer.secho(
            f'You searched for books by author with the name "{author}" so here is the result:', fg='white')

        table_headers = ['#', 'Book ID', 'Name',
                         'Author', '# Pages', 'Genre', 'Availability']
        util.formating.print_table(table_headers, search_result)
        console.print('')
    else:
        typer.secho(
            f'No book  with the name "{author}" could be found. Try again!', fg='white')
        console.print('')


@app.command("recently_added")
def recently_added(genre: Optional[str] = typer.Argument(None)):

    util.formating.show_header()

    if genre:

        search_result = util.db.sql_select(f"""
        SELECT DISTINCT  logs.book_id, books.book_name, books.book_author, books.book_number_of_pages,books.book_genre, books.book_count, logs.timestamp, users.user_name

        FROM logs
        JOIN books ON logs.book_id = books.book_id
        JOIN users on logs.user_id = users.user_id
        WHERE logs.added IS TRUE and lower(books.book_genre) = lower('{genre}')
        ORDER BY logs.timestamp DESC
        LIMIT 5;
            """, "fetchall")

        typer.secho(
            f'Here are the 5 most recently added books in the genre "{genre}": ', fg='white')

        table_headers = ['#', 'Book ID', 'Name', 'Author',
                         '# Pages', 'Genre', '', 'Availability', 'Added by']
        util.formating.print_table(table_headers, search_result, [
                                   6])  # removes colum number 6
        typer.secho('')

    else:
        search_result = util.db.sql_select(f"""
            SELECT DISTINCT  logs.book_id, books.book_name, books.book_author, books.book_number_of_pages,books.book_genre, books.book_count, logs.timestamp, users.user_name

            FROM logs
            JOIN books ON logs.book_id = books.book_id
            JOIN users on logs.user_id = users.user_id
            WHERE logs.added IS TRUE
            ORDER BY logs.timestamp DESC
            LIMIT 5;
        """, "fetchall")

        typer.secho(f'Here are the 5 most recently added books:', fg='white')
        table_headers = ['#', 'Book ID', 'Name', 'Author',
                         '# Pages', 'Genre', '', 'Availability', 'Added by']
        util.formating.print_table(table_headers, search_result, [
                                   6])  # removes colum number 6
        typer.secho(f'')






@app.command("most_read_books")
def most_read_books(genre: Optional[str] = typer.Argument(None)):

    util.formating.show_header()

    if genre:

        search_result = util.db.sql_select(f"""
            SELECT books.book_id, books.book_name, books.book_author, books.book_genre, COUNT(DISTINCT logs.user_id) as read_count
            FROM books
            JOIN logs ON books.book_id = logs.book_id
            WHERE logs.added = TRUE and lower(books.book_genre) = lower('{genre}')
            GROUP BY books.book_id
            ORDER BY read_count DESC
            LIMIT 10;
        """, "fetchall")

        typer.secho(f'Here are the 10 most read books in the genre {genre}:', fg='white')
        table_headers = ['#', 'Book ID', 'Name', 'Author', 'Genre', 'Count']
        util.formating.print_table(table_headers, search_result)
        typer.secho(f'')

    else:
        search_result = util.db.sql_select(f"""
            SELECT books.book_id, books.book_name, books.book_author, books.book_genre, COUNT(DISTINCT logs.user_id) as read_count
            FROM books
            JOIN logs ON books.book_id = logs.book_id
            WHERE logs.added = TRUE
            GROUP BY books.book_id
            ORDER BY read_count DESC
            LIMIT 10;
        """, "fetchall")

        typer.secho(f'Here are the 10 most read books:', fg='white')
        table_headers = ['#', 'Book ID', 'Name', 'Author', 'Genre', 'Count']
        util.formating.print_table(table_headers, search_result)
        typer.secho(f'')







@app.command("most_favorite_books")
def most_favorite_books(genre: Optional[str] = typer.Argument(None)):

    util.formating.show_header()

    if genre:

        search_result = util.db.sql_select(f"""
            SELECT books.book_id, books.book_name, books.book_author, books.book_genre, COUNT(DISTINCT logs.user_id) as read_count
            FROM books
            JOIN logs ON books.book_id = logs.book_id
            WHERE logs.favorited = TRUE and lower(books.book_genre) = lower('{genre}')
            GROUP BY books.book_id
            ORDER BY read_count DESC
            LIMIT 10;
        """, "fetchall")

        typer.secho(f'Here are the 10 most favorited books in the genre {genre}:', fg='white')
        table_headers = ['#', 'Book ID', 'Name', 'Author', 'Genre', 'Count']
        util.formating.print_table(table_headers, search_result)
        typer.secho(f'')

    else:
        search_result = util.db.sql_select(f"""
            SELECT books.book_id, books.book_name, books.book_author, books.book_genre, COUNT(DISTINCT logs.user_id) as read_count
            FROM books
            JOIN logs ON books.book_id = logs.book_id
            WHERE logs.favorited = TRUE
            GROUP BY books.book_id
            ORDER BY read_count DESC
            LIMIT 10;
        """, "fetchall")

        typer.secho(f'Here are the 10 most favorited books:', fg='white')
        table_headers = ['#', 'Book ID', 'Name', 'Author', 'Genre', 'Count']
        util.formating.print_table(table_headers, search_result)
        typer.secho(f'')
















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
