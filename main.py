import time
import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from typing import Optional
import inquirer


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

        choices = ['sign_up', 'sign_in', 'search_by_name',
                   'search_by_author', 'recently_added', 'most_read_books', 'most_favorite_books', 'most_read_genres', 'most_read_authors',
                   'add_book', 'borrow_book', 'return_book', 'mark_read', 'fav_book', 'my_books', 'statistics'
                   ]

    else:
        typer.secho(f"You are not logged in!", fg=typer.colors.BRIGHT_YELLOW)
        print('')
        choices = ['sign_up', 'sign_in', 'search_by_name',
                   'search_by_author', 'recently_added', 'most_read_books', 'most_favorite_books', 'most_read_genres', 'most_read_authors']

    #################################################################
    #################################################################

    ask = [inquirer.List(
        'run_command', message="What would you like to do?", choices=choices)]

    answer = inquirer.prompt(ask)

    if answer['run_command'] == "sign_up":

        username = typer.prompt("What's the username you want: ")
        sign_up(username)
    elif answer['run_command'] == "sign_in":

        username = typer.prompt("What's your username: ")
        password = typer.prompt("What's your password: ", hide_input=True)

        sign_in(username, password)
    elif answer['run_command'] == "search_by_name":

        bookName = typer.prompt("What's the book name you're looking for?")
        search_by_name(f'{bookName}')
    elif answer['run_command'] == "search_by_author":

        author = typer.prompt("What's the author you're looking for?")
        search_by_author(f'{author}')
    elif answer['run_command'] == "recently_added":

        genre = typer.prompt("Any genre in mind (optional)?", default='')
        recently_added(f'{genre}')
    elif answer['run_command'] == "most_read_books":

        genre = typer.prompt("Any genre in mind (optional)?", default='')
        most_read_books(f'{genre}')
    elif answer['run_command'] == "most_favorite_books":

        genre = typer.prompt("Any genre in mind (optional)?", default='')
        most_favorite_books(f'{genre}')
    elif answer['run_command'] == "most_read_genres":

        most_read_genres()
    elif answer['run_command'] == "most_read_authors":

        most_read_authors()
    elif answer['run_command'] == "add_book":

        add_book()
    elif answer['run_command'] == "borrow_book":

        book_id = typer.prompt(
            "What's the book id of the book you're returning?")
        borrow_book(book_id)
        pass
    elif answer['run_command'] == "return_book":

        book_id = typer.prompt(
            "What's the book id of the book you're returning?")
        return_book(book_id)
    elif answer['run_command'] == "mark_read":

        book_id = typer.prompt(
            "What's the book id that you want marked as read?")
        mark_read(book_id)
    elif answer['run_command'] == "fav_book":

        # book_id = typer.prompt("What's the book id that you want marked as read?")
        # fav_book(book_id)
        pass
    elif answer['run_command'] == "my_books":

        my_books()
    elif answer['run_command'] == "statistics":

        statistics()

    #################################################################
    #################################################################


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

        table_headers = ['Book ID', 'Name',
                         'Author', '# Pages', 'Genre', 'Book_Count']
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

        typer.secho(
            f'Here are the 10 most read books in the genre {genre}:', fg='white')
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

        typer.secho(
            f'Here are the 10 most favorited books in the genre {genre}:', fg='white')
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


@app.command("most_read_genres")
def most_read_genres():

    util.formating.show_header()

    search_result = util.db.sql_select(f"""
        SELECT books.book_genre, COUNT(DISTINCT logs.user_id) as read_count
        FROM books
        JOIN logs ON books.book_id = logs.book_id
        WHERE logs.read = TRUE
        GROUP BY books.book_genre
        ORDER BY read_count DESC
        LIMIT 5;
    """, "fetchall")

    typer.secho(f'Here are the 5 most read book genres:', fg='white')
    table_headers = ['#', 'Genre', 'Count']
    util.formating.print_table(table_headers, search_result)
    typer.secho(f'')


@app.command("most_read_authors")
def most_read_authors():

    util.formating.show_header()

    search_result = util.db.sql_select(f"""
        SELECT books.book_author, COUNT(DISTINCT logs.user_id) as read_count
        FROM books
        JOIN logs ON books.book_id = logs.book_id
        WHERE logs.read = TRUE
        GROUP BY books.book_author
        ORDER BY read_count DESC
        LIMIT 5;
    """, "fetchall")

    typer.secho(f'Here are the 5 most read book authors:', fg='white')
    table_headers = ['#', 'Author', 'Count']
    util.formating.print_table(table_headers, search_result)
    typer.secho(f'')


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
        typer.echo("")

        typer.echo("Please enter the details of the book you want to add!")
        name = typer.prompt("Name: ")
        author = typer.prompt("Author: ")
        page_count = typer.prompt("# Pages: ")
        genre = typer.prompt("Genre: ")
        book_count = 1
        search_result = util.db.sql_select(f"""
            SELECT * from books
            WHERE (lower(book_name) = lower('{name}') AND lower(book_author) = lower('{author}'))
        """, "fetchall")
        if search_result:       # if there is same book in database then update only book_count
            book_count = search_result[0][5] + 1

            util.db.sql_update(f"""
                UPDATE books
                SET book_count = {book_count}
                WHERE (lower(book_name) = lower('{name}') AND lower(book_author) = lower('{author}'))
            """)
        else:

            util.db.sql_insert(f"""
                INSERT INTO books (book_name, book_author, book_number_of_pages, book_genre, book_count)
                VALUES ('{name}', '{author}', {page_count}, '{genre}', {book_count})
            """)
        """"log the process"""
        # getting book_id
        search_result = util.db.sql_select(f"""
            SELECT book_id from books
            WHERE (lower(book_name) = lower('{name}') AND lower(book_author) = lower('{author}'))
        """, "fetchall")
        book_id = search_result[0][0]
        # getting the user id:
        user_id = util.db.sql_select(
            f"SELECT user_id from users WHERE user_name = '{session['username']}'")
        user_id = user_id[0][0]
        # adding log record
        util.db.sql_insert(f"""
            INSERT INTO logs (user_id, book_id, added)
            VALUES ('{user_id}', '{book_id}', True)
        """)
        typer.echo("Book is successfully added!", fg='green')
        typer.echo("")

    else:
        typer.secho("You need to login first.",  fg='red')
        typer.echo("")


@app.command("return_book")
def return_book(book_id: int):

    util.formating.show_header()

    if session:

        typer.secho(f"Welcome back, {session['username']}!",  fg='green')
        typer.secho(f"")

        # getting the user id:
        user_id = util.db.sql_select(
            f"SELECT user_id from users WHERE user_name = '{session['username']}'")
        user_id = user_id[0][0]

        book_borrowed_by_user = util.db.sql_select(
            f"SELECT * from logs WHERE user_id = {user_id} and borrowed=TRUE and book_id = {book_id}")

        if book_borrowed_by_user:

            util.db.sql_update(f"""
                UPDATE logs
                set borrowed=false
                WHERE user_id ={user_id} and book_id={book_id}
            """)
            typer.secho(f"Thanks for returning the book!", fg='green')
            typer.secho(f"")

        else:
            typer.secho(f"This book is not borrowed by you.", fg='red')
            typer.secho(f"")

    else:
        typer.secho("You need to login first.",  fg='red')
        typer.secho(f"")


@app.command("mark_read")
def mark_read(book_id: int):

    util.formating.show_header()

    if session:

        typer.secho(f"Welcome back, {session['username']}!",  fg='green')
        typer.secho(f"")

        # getting the user id:
        user_id = util.db.sql_select(
            f"SELECT user_id from users WHERE user_name = '{session['username']}'")
        user_id = user_id[0][0]

        already_marked_as_read = util.db.sql_select(
            f"SELECT * from logs WHERE user_id = {user_id} and read=TRUE and book_id = {book_id}")

        if already_marked_as_read:

            # util.db.sql_update(f"""
            #     UPDATE logs
            #     set borrowed=false
            #     WHERE user_id ={user_id} and book_id={book_id}
            # """)

            book_name = util.db.sql_select(
                f"SELECT book_name from books WHERE book_id = {book_id}")
            book_name = book_name[0][0]

            typer.secho(
                f"Book id {book_id} ({book_name}) is already marked as read!", fg='green')
            typer.secho(f"")

        else:

            book_exist = util.db.sql_select(
                f"SELECT * from books WHERE book_id = '{book_id}'")

            if book_exist:

                # adding log record
                util.db.sql_insert(f"""
                    INSERT INTO logs (user_id, book_id, read)
                    VALUES ('{user_id}', '{book_id}', True)
                """)

                book_name = util.db.sql_select(
                    f"SELECT book_name from books WHERE book_id = {book_id}")
                book_name = book_name[0][0]

                typer.secho(
                    f"Marked book id {book_id} ({book_name}) as read!", fg='green')
                typer.secho(f"")
            else:
                typer.secho(
                    f"Book with id {book_id} could not be found", fg='red')
                typer.secho(f"")

    else:
        typer.secho("You need to login first.",  fg='red')


@app.command("my_books")
def my_books():
    util.formating.show_header()
    if session:
        typer.secho(f"Welcome back, {session['username']}!",  fg='green')
        typer.secho(f"")

        # getting the user id:
        user_id = util.db.sql_select(
            f"SELECT user_id from users WHERE user_name = '{session['username']}'")
        user_id = user_id[0][0]

        # Read books
        # ----------------------------------------------------------------------
        search_result = util.db.sql_select(f"""
            SELECT books.book_id, books.book_name, books.book_author, books.book_number_of_pages, books.book_genre FROM books 
            RIGHT JOIN logs ON books.book_id = logs.book_id 
            WHERE (logs.user_id = {user_id} AND logs.read = true)
        """, "fetchall")
        if search_result:
            typer.secho(f'Here are all the books you read', fg='white')
            table_headers = ['#', 'Book ID', 'Name',
                             'Author', '# Pages', 'Genre']
            util.formating.print_table(table_headers, search_result)
            typer.secho(f'')

        # Favorite books
        # ---------------------------------------------------------------------------
        search_result = util.db.sql_select(f"""
            SELECT books.book_id, books.book_name, books.book_author, books.book_number_of_pages, books.book_genre FROM books 
            RIGHT JOIN logs ON books.book_id = logs.book_id 
            WHERE (logs.user_id = {user_id} AND logs.favorited = true)
        """, "fetchall")
        if search_result:
            typer.secho(f'And the books you have favorited', fg='white')
            table_headers = ['#', 'Book ID', 'Name',
                             'Author', '# Pages', 'Genre']
            util.formating.print_table(table_headers, search_result)
            typer.secho(f'')

    else:
        typer.secho("You need to login first.",  fg='red')


@app.command("statistics")
def statistics():
    util.formating.show_header()

    if session:
        typer.secho(f"Welcome back, {session['username']}!",  fg='green')

        # getting the user id:
        user_id = util.db.sql_select(
            f"SELECT user_id from users WHERE user_name = '{session['username']}'")
        user_id = user_id[0][0]

        search_result = util.db.sql_select(f"""
            SELECT COUNT(DISTINCT books.book_id), 
                COUNT(DISTINCT books.book_author), 
                COUNT(DISTINCT books.book_genre), 
                SUM(books.book_number_of_pages) FROM books 
            RIGHT JOIN logs ON books.book_id = logs.book_id 
            WHERE (logs.user_id = {user_id} AND logs.read = true)
        """, "fetchone")

        # making table to print
        if search_result:
            table = []
            fields = ['Books', 'Authors', 'Genres', 'Total pages']
            for i in range(4):
                row = f"{fields[i]} you read", search_result[i]
                table.append(row)

            typer.secho(f'')
            table_headers = ['Statistics', 'Number']
            util.formating.print_table(table_headers, table, show_count=False)
            typer.secho(f'')

    else:
        typer.secho("You need to login first.",  fg='red')


@app.command("borrow_book")
def borrow_book(book_id: int):
    util.formating.show_header()

    if session:
        typer.secho(
            f"Hello, {session['username']}! you are logged in",  fg='green')
        typer.secho('')

        user_name = session['username']

        book_available = util.db.sql_select(
            f"""SELECT book_count FROM books WHERE book_id = {book_id} AND book_count > 0""")

        if not book_available:
            typer.secho(f'sorry book {book_id} is not available', fg='red')
            typer.secho(f'')
        else:
            book_already_borrowed = util.db.sql_select(
                f"""SELECT 1 FROM logs WHERE borrowed = TRUE AND book_id = {book_id} AND user_id = (SELECT user_id FROM users WHERE user_name = '{user_name}')""")
            if book_already_borrowed:
                typer.secho(f'you already borrowed one copy bro', fg='red')
                typer.secho(f'')
            else:
                query_1 = f"""
                INSERT INTO logs (user_id, book_id, borrowed)
                SELECT u.user_id, b.book_id, TRUE
                FROM users u, books b
                WHERE u.user_name = '{user_name}' 
                  AND b.book_id = '{book_id}' 
                  AND b.book_count > 0 
                  AND NOT EXISTS (
                    SELECT 1
                    FROM logs l
                    WHERE l.borrowed = TRUE AND l.book_id = {book_id}
                  );
                """
                util.db.sql_insert(query_1)

                query_2 = f"""
                UPDATE books 
                SET book_count = book_count - 1 
                WHERE book_id = {book_id} AND book_count > 0;
                """
                util.db.sql_insert(query_2)

                query_3 = f"""
                SELECT book_id, borrowed 
                FROM logs 
                WHERE book_id = {book_id} AND user_id = (SELECT user_id FROM users WHERE user_name = '{user_name}');
                """
                search_result = util.db.sql_select(query_3)
                typer.secho(
                    f"Thanks, {session['username']} for borrowing book {book_id}",  fg='green')
                table_headers = ['book_id', 'status']
                util.formating.print_table(
                    table_headers, search_result, show_count=False)
                typer.secho(f'')

    else:
        typer.secho("You need to login first.",  fg='red')
        typer.secho(f'')


@app.command("fav_book")
def fav_book(book_id: int, user_name: str,):

    if session:

        typer.secho(
            f"Hello, {session['username']}! you are logged in",  fg='green')

        Favored = util.db.sql_select(
            f"""SELECT l.user_id FROM logs l WHERE l.favorited = True AND l.book_id = {book_id}""")
        if not Favored:
            util.db.sql_insert(
                f""" 
            UPDATE logs AS l 
            SET favorited = True
            FROM users as u , books as b
            WHERE l.user_id = u.user_id AND l.book_id = b.book_id AND u.user_name = '{user_name}' AND b.book_id = '{book_id}' ;
                """
            )

            typer.secho(
                f"Thanks, {session['username']}! you have added book {book_id} as the faviorte book",  fg='green')
        else:
            typer.secho(f'the book {book_id} is already your faviorte book')
    #######################################################
    else:
        typer.secho("You need to login first.",  fg='red')
        typer.secho(f"")


#######################################################
#######################################################
# ~~~~~~~~~~~~~~~ THE END ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#######################################################
#######################################################
@app.command("showme")
def showme():
    query_1 = f"""
    SELECT *
    FROM logs
    """
    selected = util.db.sql_select(query_1)
    table_headers = ['#', 'Log_ID', 'User_ID', 'Book_ID',
                     'Borrowed', 'READ', 'Favorited', 'Added', 'Timestamp']
    # removes colum number 6
    util.formating.print_table(table_headers, selected)
    typer.secho(f'')


if __name__ == "__main__":
    console.clear()  # clears the terminal of any text.
    app()
