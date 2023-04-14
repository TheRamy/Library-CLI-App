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
    host="111111",
    database="library_cli_app",
    user="11111111",
    password="111111"
)
conn.autocommit = True


@app.get("/books/")
def all_books():
    cursor = conn.cursor()
    query = "SELECT * FROM public.books"
    cursor.execute(query)
    books = cursor.fetchall()
    cursor.close()
    return books


@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
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
    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    cursor = conn.cursor()
    query = "DELETE FROM public.books WHERE book_id = %s"
    cursor.execute(query, (book_id,))
    deleted_rows = cursor.rowcount
    cursor.close()
    if deleted_rows:
        return {"msg": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")


@app.post("/books/")
def add_book(book: Book):
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


uvicorn.run(app, host="0.0.0.0", port=8000)



