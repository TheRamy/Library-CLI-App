import psycopg2
from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi

from pydantic import BaseModel
import uvicorn


app = FastAPI()


class Book(BaseModel):
    book_name: str
    book_author: str
    book_number_of_pages: int
    book_genre: str
    book_count: int


# Connect to the database
conn = psycopg2.connect(
    host="class8.my.to",
    database="library_cli_app",
    user="class8",
    password="123"
)
conn.autocommit = True



def authenticate(username: str, password: str):
    cursor = conn.cursor()
    query = "SELECT * FROM public.users WHERE user_name = %s AND user_password = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    cursor.close()
    return user




@app.post("/users/")
def add_user(user_name: str, user_password: str):
    cursor = conn.cursor()
    query = """
        INSERT INTO public.users (user_name, user_password)
        VALUES (%s, %s)
    """
    cursor.execute(query, (user_name, user_password))
    cursor.close()
    return {"msg": "User added successfully"}


@app.get("/logs/")
def all_logs():
    cursor = conn.cursor()
    query = "SELECT * FROM public.logs ORDER BY log_id"
    cursor.execute(query)
    logs = cursor.fetchall()
    cursor.close()
    return logs


@app.get("/books/")
def all_books():
    cursor = conn.cursor()
    query = "SELECT * FROM public.books ORDER BY book_id"
    cursor.execute(query)
    books = cursor.fetchall()
    cursor.close()
    return books


@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book, username: str, password: str):
    user = authenticate(username, password)
    if user:
        cursor = conn.cursor()
        query = """
            UPDATE public.books
            SET book_name = %s, book_author = %s, book_number_of_pages = %s, book_genre = %s, book_count = %s
            WHERE book_id = %s
        """
        cursor.execute(query, (book.book_name, book.book_author,
                       book.book_number_of_pages, book.book_genre, book.book_count, book_id))
        updated_rows = cursor.rowcount
        cursor.close()
        if updated_rows:
            return {"msg": "Book updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="Book not found")
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")


@app.delete("/books/{book_id}")
def delete_book(book_id: int, username: str, password: str):
    # Authenticate user first
    if not authenticate(username, password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    cursor = conn.cursor()
    
    # Delete references to the book in the "logs" table
    query = "DELETE FROM public.logs WHERE book_id = %s"
    cursor.execute(query, (book_id,))
    
    # Delete the book from the "books" table
    query = "DELETE FROM public.books WHERE book_id = %s"
    cursor.execute(query, (book_id,))
    
    deleted_rows = cursor.rowcount
    cursor.close()
    if deleted_rows:
        return {"msg": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")




@app.post("/books/")
def add_book(book: Book, username: str, password: str):
    # Authenticate user
    cursor = conn.cursor()
    query = "SELECT * FROM public.users WHERE user_name = %s AND user_password = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    cursor.close()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Add book to database
    cursor = conn.cursor()
    query = """
        INSERT INTO public.books (book_name, book_author, book_number_of_pages, book_genre, book_count)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (book.book_name, book.book_author,
                   book.book_number_of_pages, book.book_genre, book.book_count))
    cursor.close()
    return {"msg": "Book added successfully"}








def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Library CLI App API",
        version="1.0.0",
        description='This is an API for the app here: <a href="https://github.com/TheRamy/Library-CLI-App">https://github.com/TheRamy/Library-CLI-App</a> <br> It uses the same database used in the CLI app so you will also see the updates reflected in the CLI.',
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# uvicorn.run(app, host="0.0.0.0", port=8000)


uvicorn.run(
    app,
    host="0.0.0.0",
    port=443,
    ssl_keyfile="/etc/letsencrypt/live/class8.my.to/privkey.pem",
    ssl_certfile="/etc/letsencrypt/live/class8.my.to/fullchain.pem"
)


# scp server.py root@ramy-srv01.ftp.sh:/root/
# screen -dmS server bash -c 'python3 server.py'
