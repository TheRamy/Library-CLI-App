from rich.console import Console
import typer
import time
import psycopg2
import inquirer
import util.db


console = Console()

console.clear()

header = '''
██████  ███████ ██████  ██    ██  ██████   ██████  ██ ███    ██  ██████  
██   ██ ██      ██   ██ ██    ██ ██       ██       ██ ████   ██ ██       
██   ██ █████   ██████  ██    ██ ██   ███ ██   ███ ██ ██ ██  ██ ██   ███ 
██   ██ ██      ██   ██ ██    ██ ██    ██ ██    ██ ██ ██  ██ ██ ██    ██ 
██████  ███████ ██████   ██████   ██████   ██████  ██ ██   ████  ██████   
    '''
print(header)

# read connection parameters
params = util.db.db_config()

# connect to the PostgreSQL server
# print('Connecting to the PostgreSQL database...')
conn = psycopg2.connect(**params)
# create a cursor


# Define function to retrieve book data from database
def get_books():
    cur = conn.cursor()
    cur.execute("SELECT book_id, book_name, book_author, book_genre FROM books")
    books = cur.fetchall()
    return books

# Define function to prompt user for book selection


def select_book(books):
    questions = [
        inquirer.List('book',
                      message="Select a book to view details:",
                      choices=books)
    ]
    answers = inquirer.prompt(questions)
    return answers['book']

# Define function to display book details


def display_book(book):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM books WHERE book_id=%s", (book[0],))
        book_data = cur.fetchone()
        book_id, book_name, book_author, book_number_of_pages, book_genre, book_count = book_data

        cur.execute("""
            SELECT user_name 
            FROM logs 
            JOIN users ON logs.user_id = users.user_id 
            WHERE logs.book_id = %s AND logs.added = true
        """, (book_id,))
        row = cur.fetchone()
        added_by = row[0] if row is not None else None

        cur.execute("""
            SELECT user_name 
            FROM logs 
            JOIN users ON logs.user_id = users.user_id 
            WHERE logs.book_id = %s AND logs.read = true
        """, (book_id,))
        readers = [row[0] for row in cur.fetchall()]

        cur.execute("""
            SELECT user_name 
            FROM logs 
            JOIN users ON logs.user_id = users.user_id 
            WHERE logs.book_id = %s AND logs.borrowed = true
        """, (book_id,))
        borrowers = [row[0] for row in cur.fetchall()]

        cur.execute("""
            SELECT user_name 
            FROM logs 
            JOIN users ON logs.user_id = users.user_id 
            WHERE logs.book_id = %s AND logs.favorited = true
        """, (book_id,))
        favorited_by = [row[0] for row in cur.fetchall()]

    print("Book ID:", book_id)
    print("Name:", book_name)
    print("Author:", book_author)
    print("Number of Pages:", book_number_of_pages)
    print("Genre:", book_genre)
    print("Count:", book_count)
    if added_by is not None:
        print("Added by:", added_by)
    print("Read by:", ", ".join(readers))
    print("Borrowed by:", ", ".join(borrowers))
    print("Favorited by:", ", ".join(favorited_by))


# Get list of books
books = get_books()

# Loop until user chooses to exit
while True:
    # Prompt user to select a book
    book = select_book(books)

    # Display book details
    display_book(book)

    # Prompt user to continue or exit
    again = typer.prompt(
        "Press enter to search again, or N to exit: ", default=True)
    if not again:
        break

# Close database connection
conn.close()
